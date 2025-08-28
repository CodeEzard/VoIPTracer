"""FastAPI endpoint for uploading pcaps and running analysis."""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from pathlib import Path
from typing import Dict, Any

from . import capture, parser, agg, analyze, viz

app = FastAPI(title="VoIP Meta Tracer", version="1.0.0")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "VoIP Meta Tracer API", "status": "healthy"}


@app.post("/upload-pcap")
async def upload_pcap(file: UploadFile = File(...), limit: int = 1000) -> Dict[str, Any]:
    """Upload pcap file and run VoIP metadata analysis.
    
    Args:
        file: Uploaded pcap file
        limit: Max packets to process
    
    Returns:
        JSON with analysis results
    """
    if not file.filename.endswith(('.pcap', '.pcapng')):
        raise HTTPException(status_code=400, detail="File must be .pcap or .pcapng")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pcap') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    try:
        # Run analysis pipeline
        result = run_analysis_pipeline(tmp_path, limit)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/analyze-file")
async def analyze_file(file_path: str, limit: int = 1000) -> Dict[str, Any]:
    """Analyze existing pcap file on server.
    
    Args:
        file_path: Path to pcap file on server
        limit: Max packets to process
    
    Returns:
        JSON with analysis results
    """
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        result = run_analysis_pipeline(file_path, limit)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


def run_analysis_pipeline(pcap_path: str, limit: int = 1000) -> Dict[str, Any]:
    """Run the complete analysis pipeline on a pcap file.
    
    Args:
        pcap_path: Path to pcap file
        limit: Max packets to process
    
    Returns:
        Dict with analysis results
    """
    # Step 1: Capture metadata
    raw_packets = list(capture.read_pcap(pcap_path, limit=limit))
    
    if not raw_packets:
        return {
            "status": "no_voip_packets",
            "message": "No VoIP packets found in pcap",
            "calls": [],
            "summary": {"total_calls": 0, "anomalies": 0, "anomaly_rate": 0.0}
        }
    
    # Step 2: Parse and group by call
    calls = parser.attach_meta_from_raw_packets(raw_packets)
    
    # Step 3: Convert to DataFrame
    df = agg.calls_to_dataframe(calls)
    if df.empty:
        return {
            "status": "no_calls",
            "message": "No complete calls found",
            "calls": [],
            "summary": {"total_calls": 0, "anomalies": 0, "anomaly_rate": 0.0}
        }
    
    # Step 4: Add features and filter
    df = agg.add_derived_features(df)
    df = agg.filter_calls(df)
    
    # Step 5: Anomaly detection
    df = analyze.detect_anomalies(df)
    df = analyze.flag_suspicious_patterns(df)
    anomaly_summary = analyze.summarize_anomalies(df)
    
    # Step 6: Export results (optional - for API we just return JSON)
    # viz.export_csv(df, "out/api_results.csv")
    
    # Convert DataFrame to JSON-serializable format
    calls_json = df.to_dict('records')
    
    # Build graph for statistics
    graph = viz.build_call_graph(df)
    graph_stats = {
        "nodes": len(graph.nodes),
        "edges": len(graph.edges),
        "components": len(list(graph.connected_components())) if graph.nodes else 0
    }
    
    return {
        "status": "success",
        "calls": calls_json,
        "summary": anomaly_summary,
        "graph_stats": graph_stats,
        "packets_processed": len(raw_packets)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
