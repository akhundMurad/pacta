from pacta.reporting._json import dumps_deterministic
from pacta.reporting.types import Report


class JsonReportRenderer:
    """
    Machine-readable JSON output (CI, SaaS ingestion).
    """

    def render(self, report: Report) -> str:
        return dumps_deterministic(report.to_dict()) + "\n"
