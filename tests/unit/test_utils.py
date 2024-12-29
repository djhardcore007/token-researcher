import pytest
from src.utils import save_report, load_multiple_reports, load_single_report, reports_to_csv
from src.schema import Report


TEST_FILES_DIR = 'tests/test_files'
TEST_FILE_PATH = f'{TEST_FILES_DIR}/report_solana_JAIL_20241229_004744.json'


def test_save_report(tmpdir):
    report = load_single_report(TEST_FILE_PATH)
    save_report(report, str(tmpdir.join("test_report.json")))


def test_load_single_report():
    report = load_single_report(TEST_FILE_PATH)
    assert isinstance(report, Report)

@pytest.fixture
def get_multiple_reports():
    json_paths = [f'{TEST_FILES_DIR}/report_solana_JAIL_20241229_004744.json']
    reports = load_multiple_reports(json_paths)
    assert len(reports) > 0
    assert isinstance(reports[0], Report)
    yield reports


def test_reports_to_csv(get_multiple_reports, tmpdir):
    reports = get_multiple_reports
    reports_to_csv(reports, str(tmpdir.join("test_reports.csv")))
