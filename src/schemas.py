from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, validator


class CDR(BaseModel):
	"""Call Detail Record schema.

	Fields:
	  - subscriber: caller/subscriber identifier
	  - called: called party identifier
	  - call_type: VOICE/SMS/etc.
	  - start_time, end_time: datetimes (ISO8601 strings accepted)
	"""

	subscriber: str
	called: str
	call_type: str
	start_time: datetime
	end_time: datetime

	@validator("end_time")
	def end_must_be_after_start(cls, v: datetime, values: dict[str, Any]) -> datetime:
		start = values.get("start_time")
		if start is not None and v < start:
			raise ValueError("end_time must be >= start_time")
		return v


class IPDR(BaseModel):
	"""IP Data Record schema.

	Fields:
	  - subscriber: subscriber identifier
	  - destination_ip: destination IPv4/IPv6 as string
	  - protocol: TCP/UDP (normalized to upper-case)
	  - dst_port: integer port
	  - start_time, end_time: datetimes
	"""

	subscriber: str
	destination_ip: str
	protocol: str = Field(..., description="Protocol name, e.g. TCP or UDP")
	dst_port: int
	start_time: datetime
	end_time: datetime

	@validator("protocol", pre=True)
	def norm_protocol(cls, v: Any) -> str:
		return str(v).upper()

	@validator("dst_port")
	def port_must_be_valid(cls, v: int) -> int:
		if not (0 <= v <= 65535):
			raise ValueError("dst_port must be in 0..65535")
		return v

	@validator("end_time")
	def end_must_be_after_start(cls, v: datetime, values: dict[str, Any]) -> datetime:
		start = values.get("start_time")
		if start is not None and v < start:
			raise ValueError("end_time must be >= start_time")
		return v


__all__ = ["CDR", "IPDR"]
