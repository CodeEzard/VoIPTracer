"""Visualization and export functionality."""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional


def export_csv(df: pd.DataFrame, output_path: str = "out/calls.csv") -> None:
    """Export DataFrame to CSV.
    
    Args:
        df: Call DataFrame to export
        output_path: Output CSV file path
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Exported {len(df)} calls to {output_path}")


def build_call_graph(df: pd.DataFrame) -> nx.Graph:
    """Build networkx graph from call data.
    
    Args:
        df: Call DataFrame
    
    Returns:
        NetworkX graph with IPs as nodes, calls as edges
    """
    G = nx.Graph()
    
    for _, row in df.iterrows():
        src_ips = row['src_ips'].split(',') if row['src_ips'] else []
        dst_ips = row['dst_ips'].split(',') if row['dst_ips'] else []
        
        # Add nodes
        for ip in src_ips + dst_ips:
            if ip.strip():
                G.add_node(ip.strip())
        
        # Add edges between src and dst IPs
        for src_ip in src_ips:
            for dst_ip in dst_ips:
                if src_ip.strip() and dst_ip.strip() and src_ip != dst_ip:
                    edge_data = {
                        'call_id': row['call_id'],
                        'duration': row['duration_s'],
                        'packets': row['total_pkts'],
                        'is_anomaly': row.get('is_anomaly', False)
                    }
                    G.add_edge(src_ip.strip(), dst_ip.strip(), **edge_data)
    
    return G


def plot_call_graph(G: nx.Graph, output_path: str = "out/call_graph.png", 
                   figsize: tuple = (12, 8)) -> None:
    """Plot and save call graph visualization.
    
    Args:
        G: NetworkX graph
        output_path: Output image file path
        figsize: Figure size tuple
    """
    if len(G.nodes) == 0:
        print("No nodes to plot")
        return
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=figsize)
    
    # Layout
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=300, alpha=0.7)
    
    # Draw normal edges
    normal_edges = [(u, v) for u, v, d in G.edges(data=True) 
                   if not d.get('is_anomaly', False)]
    nx.draw_networkx_edges(G, pos, edgelist=normal_edges, 
                          edge_color='gray', alpha=0.5)
    
    # Draw anomalous edges in red
    anomaly_edges = [(u, v) for u, v, d in G.edges(data=True) 
                    if d.get('is_anomaly', False)]
    if anomaly_edges:
        nx.draw_networkx_edges(G, pos, edgelist=anomaly_edges, 
                              edge_color='red', alpha=0.8, width=2)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=8)
    
    plt.title(f"VoIP Call Graph ({len(G.nodes)} IPs, {len(G.edges)} calls)")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved graph visualization to {output_path}")


def export_graph_stats(G: nx.Graph, output_path: str = "out/graph_stats.txt") -> None:
    """Export graph statistics to text file.
    
    Args:
        G: NetworkX graph
        output_path: Output text file path
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    stats = []
    stats.append(f"Graph Statistics")
    stats.append(f"================")
    stats.append(f"Nodes (IPs): {len(G.nodes)}")
    stats.append(f"Edges (calls): {len(G.edges)}")
    stats.append(f"Connected components: {nx.number_connected_components(G)}")
    
    if len(G.nodes) > 0:
        stats.append(f"Average degree: {sum(dict(G.degree()).values()) / len(G.nodes):.2f}")
        
        # Top nodes by degree
        degree_centrality = nx.degree_centrality(G)
        top_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        stats.append(f"\nTop nodes by degree:")
        for node, centrality in top_nodes:
            stats.append(f"  {node}: {centrality:.3f}")
    
    # Anomaly stats
    anomaly_edges = sum(1 for u, v, d in G.edges(data=True) if d.get('is_anomaly', False))
    stats.append(f"\nAnomalous calls: {anomaly_edges}")
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(stats))
    
    print(f"Exported graph stats to {output_path}")


def create_summary_report(df: pd.DataFrame, anomaly_summary: dict, 
                         output_path: str = "out/summary.txt") -> None:
    """Create a text summary report.
    
    Args:
        df: Call DataFrame
        anomaly_summary: Dict from analyze.summarize_anomalies()
        output_path: Output text file path
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    report = []
    report.append("VoIP Metadata Analysis Summary")
    report.append("=" * 40)
    report.append(f"Total calls analyzed: {len(df)}")
    
    if not df.empty:
        report.append(f"Time range: {df['start_dt'].min()} to {df['start_dt'].max()}")
        report.append(f"Total duration: {df['duration_s'].sum():.1f} seconds")
        report.append(f"Average call duration: {df['duration_s'].mean():.1f} seconds")
        report.append(f"Total packets: {df['total_pkts'].sum()}")
        report.append(f"Total bytes: {df['total_bytes'].sum()}")
    
    report.append(f"\nAnomaly Detection:")
    report.append(f"Anomalous calls: {anomaly_summary.get('anomalies', 0)}")
    report.append(f"Anomaly rate: {anomaly_summary.get('anomaly_rate', 0):.1%}")
    
    # Add flag summaries
    for key, value in anomaly_summary.items():
        if key.endswith('_count') and value > 0:
            flag_name = key.replace('_count', '').replace('_', ' ')
            report.append(f"{flag_name.title()}: {value}")
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"Created summary report: {output_path}")
