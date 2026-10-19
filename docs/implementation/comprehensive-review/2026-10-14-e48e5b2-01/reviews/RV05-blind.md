# RV05 blind source notes

Candidate/fixes unread at this write. S=e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1; Portal T=10b6c871bb89cce4f2bdc1c4cdaa91e500111ceb; AiiDA A=69aa1309c8465a838e4778b9dff464a306229f01. N=6 card; source only.

1. T `service.py::AiidaService` executor max_workers=1 owns profile load, explicit loop, all ORM operation calls; calls wait synchronously on Future.result with no timeout. OPERATIONS finite allowlist, executor queue capacity not bounded by this source.
2. `open_artifact` enters context on actor; `_ArtifactReader.read/seek` dispatch through actor; finally dispatches context exit back to actor. Reads limited 65536 bytes but blocking backend read has no deadline.
3. `close` queues unload_profile/asyncgens shutdown/loop close then executor.shutdown(wait=True). Running blocked operation delays profile unload and shutdown; cancel_futures affects pending tasks after the waited shutdown Future, not running backend task.
4. `api.py::ClosingStreamingResponse.__call__` finally shield runs generator.close in threadpool; ordinary disconnect cleanup exists. Generator close while it is executing a stalled read is not proof of prompt cancellation and needs dedicated negative fixture; no production hang asserted.
5. `ExportStore._prepare` opens bound source handles, builds spool, checks cancellation via progress callback; `close` sets event then waits executor. It cannot preempt a source backend blocked inside actor Future/read. Lifespan closes export first then service, so stalled export delays whole shutdown.
6. Tests catalogue named thread ownership, reader-error cleanup, stream disconnect and export cancellation assertions; execution unmeasured. Independent distinguishing fixture would hold backend read on an event, issue disconnect/export.close, bound observed wait and prove explicit limitation, then release read to clean resources. No arbitrary unsafe concurrent profile unload proposal.

M04 six selected failure boundaries not complete whole service coverage; M13 state graph only, numeric CFG unknown. No responsiveness deadline promise justified from serialized ownership alone.
