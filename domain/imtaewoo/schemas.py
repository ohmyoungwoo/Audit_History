from __future__ import annotations
from pydantic import BaseModel
from enum import Enum
import datetime


class BaseOrmModel(BaseModel):
    class Config:
        orm_mode = True


class Preset(BaseModel):
    PRESET_SIGNAL: str
    PRESET_RESULT: str


class PresetOptions(BaseModel):
    options: str


class PresetFootnote(BaseModel):
    PRESET_FOOTNOTE: str

    class Config:
        orm_mode = True


class TableName(str, Enum):
    prod_corp = "prod_corp"
    odm = "odm"
    model = "model"


class RequestType(str, Enum):
    check = "check"
    download = "download"


class PresetTable(BaseModel):
    id: int
    product: str
    region: str
    parts: str
    report_idx: int
    hazard_idx: int
    yoy: str
    before2month: str
    before1month: str
    thismonth: str
    target: str
    ffr_recommend: str
    hzd_recommend: str
    signal: str


class PresetMeta(BaseModel):
    TV_MAX_DT_FFR_FDR_RPT: str | None
    TV_MAX_DT_FFR: str | None
    TV_MAX_DT_FDR: str | None
    TV_MAX_DT_HAZARD: str | None
    TV_MAX_DT_SVC_CNT: str | None
    AV_MAX_DT_FFR_FDR_RPT: str | None
    AV_MAX_DT_FFR: str | None
    AV_MAX_DT_FDR: str | None
    AV_MAX_DT_HAZARD: str | None
    AV_MAX_DT_SVC_CNT: str | None

    class Config:
        orm_mode = True


class VendorName(BaseModel):
    id: int
    vendor_code: str
    vendor_name: str

    class Config:
        orm_mode = True


class PenaltyBase(BaseModel):
    issue_date: datetime.date
    penalty_date: datetime.date | None
    heqm_code: str | None
    document_type: str
    reason_code: str
    division_name: str
    category_code: str
    # vendor_code: str
    vendor_code: str | None
    vendor_name: str
    part_name: str
    manager_name: str
    contents: str | None
    status: str


class PenaltyCreate(PenaltyBase):
    files: list[dict] = []


class PenaltyAttach(BaseModel):
    id: int
    name: str
    status: str
    file_path: str
    file_type: str
    file_size: str
    created_by: str
    created_date: datetime.datetime
    last_modified_date: datetime.datetime
    history_id: int

    class Config:
        orm_mode = True


class Penalty(PenaltyBase):
    id: int
    created_date: datetime.datetime
    created_by: str
    modified_date: datetime.datetime | None
    modified_by: str | None
    files: list[PenaltyAttach] = []

    class Config:
        orm_mode = True


class DashboardTableForParts(BaseModel):
    IDX: int | None
    PRODUCT_DIVIDE1: str | None
    GMES_MODULE_PROD_SITE: str | None
    GMES_PANEL_PROD_SITE: str | None
    GMES_PANEL_MAKER: str | None
    GMES_PSU_MAKER: str | None
    GMES_REMOCON_MAKER: str | None
    PROD_CORP: str | None
    INCH: str | None
    PROD_QTY: int | None
    SVC_QTY: int | None
    Y_2: float | None
    Y_1: float | None
    Y_0: float | None
    M_2: float | None
    M_1: float | None
    M_0: float | None
    YoY: str | None
    MoM: str | None
    YoY_SIGNAL: str | None
    MoM_SIGNAL: str | None
    ToT_SIGNAL: str | None
    FIXED_FDR_PRESET_IDX: int | None
    PASSED_FDR_PRESET_IDX: int | None
    HAZARD_PRESET_IDX: int | None
    FIXED_FDR_HEADER: str | None
    FIXED_FDR_GROUP: str | None
    PASSED_LEVEL2_GROUP: str | None
    HAZARD_GROUP: str | None

    class Config:
        orm_mode = True


class DashboardTableForModels(BaseModel):
    IDX: int | None
    CONTINENT: str | None
    SALES_CORP: str | None
    PROD_GROUP: str | None
    MODEL_GROUP: str | None
    BASE_GROUP: str | None
    PASSED_MON: str | None
    MODEL_FDR_M0: float | None
    BASE_FDR: float | None
    MODEL_FDR_M1: float | None
    MODEL_FDR_M2: float | None
    YoY: float | None
    MoM_M1: float | None
    MoM_M2: float | None
    EXCEPT: str | None
    EXCEPT_DESC: str | None
    YoY_SIGNAL: str | None
    MoM_M1_SIGNAL: str | None
    MoM_M2_SIGNAL: str | None
    ToT_SIGNAL: str | None
    PASSED_FDR_PRESET_IDX: int | None
    HAZARD_PRESET_IDX: int | None
    PASSED_LEVEL1_GROUP: str | None
    PASSED_LEVEL2_GROUP: str | None
    HAZARD_GROUP: str | None

    class Config:
        orm_mode = True


class AuditBase(BaseModel):
    start_date: datetime.date
    end_date: datetime.date | None
    org_name: str | None
    vendor_code: str
    vendor_name: str
    division_name: str
    category_code: str
    part_name: str
    audit_type: str
    phases: int
    manager_name: str
    common_score: float
    expertise_score: float
    total_score: float
    grade: str
    orig_file_name: str
    file_path: str
    file_size: int


class AuditCommonScore(BaseModel):
    order: int
    item: str
    score: str

    class Config:
        orm_mode = True


class AuditExpertiseScore(BaseModel):
    order: int
    item: str
    score: str

    class Config:
        orm_mode = True


class AuditCounterMeasure(BaseModel):
    id: int
    item: str
    points: str
    measures: str | None
    completion_date: datetime.date | None
    review_result: str | None
    status: str
    importance: str

    class Config:
        orm_mode = True


class Audit(AuditBase):
    id: int
    created_date: datetime.datetime
    created_by: str
    common_detail: list[AuditCommonScore] = []
    expertise_detail: list[AuditExpertiseScore] = []
    countermeasure: list[AuditCounterMeasure] = []

    class Config:
        orm_mode = True


class SalesDashboardIssueCreate(BaseModel):
    id: str
    detail: str


class Permission(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    password: str


class UserInfo(UserBase):
    name: str
    title: str
    employeeNumber: str | None
    department: str
    office: str
    mobile: str
    is_staff: bool


class UserRole(UserInfo):
    is_active: bool
    is_superuser: bool
    permissions: list[Permission] = []

    class Config:
        orm_mode = True


class Event(str, Enum):
    notify = "notify"
    message = "message"
    mutate = "mutate"


class PresetDistinct(str, Enum):
    CONTINENT = "CONTINENT"
    PROD_GROUP = "PROD_GROUP"
    MODEL_GROUP = "MODEL_GROUP"
    SALES_CORP = "SALES_CORP"
    BASE_GROUP = "BASE_GROUP"
    PASSED_MON = "PASSED_MON"


class EventProps(BaseModel):
    usernames: list[str]
    event: Event
    data: str


class ProcessDefectRateValues(BaseModel):
    index: datetime.date
    defect_qty: int
    prod_qty: int
    rate: float
    # month: datetime.date
    err_rate: float
    err_flag: bool


class ProcessDefectRateGroups(BaseModel):
    group: str
    day: list[ProcessDefectRateValues] = []
    week: list[ProcessDefectRateValues] = []
    month: list[ProcessDefectRateValues] = []
    max_limit: float


class ProcessDefectRate(BaseModel):
    __root__: list[ProcessDefectRateGroups]
    
    
class ProcessDefectRateValuesSSI(BaseModel):
    DT: datetime.date
    DEF_SEC_TP_NAME: str
    defect_qty: int
    prod_qty: int
    rate: float | None
    # month: datetime.date
    err_rate: float | None
    err_flag: bool

    
class ProcessDefectRateGroupsSSI(BaseModel):
    group: str
    day: list[ProcessDefectRateValuesSSI] = []
    week: list[ProcessDefectRateValuesSSI] = []
    month: list[ProcessDefectRateValuesSSI] = []
    max_limit: float

    
class ProcessDefectRateSSI(BaseModel):
    __root__: list[ProcessDefectRateGroupsSSI]    


class ProcessDetailDefectRateIndex(BaseModel):
    index: datetime.date
    defect_qty: int
    prod_qty: int
    rate: float | None
    err_rate: float | None


class ProcessDetailDefectRate(BaseModel):
    __root__: list[ProcessDetailDefectRateIndex]


class ProcessDetailDefectRateIndexSSI(BaseModel):
    index: datetime.date
    DT: datetime.date
    DEF_SEC_TP_NAME: str
    defect_qty: int
    prod_qty: int
    rate: float | None
    month: datetime.date
    # lqc_def_qty: int  # JS 1104
    # self_def_qty: int  # JS 1104
    # lqc_def_qty_rate: float | None
    # self_def_qty_rate: float | None
    err_rate: float | None
    err_flag: bool

class ProcessDetailDefectRateSSI(BaseModel):
    __root__: list[ProcessDetailDefectRateIndexSSI]
    
    
class ColumnFilter(BaseModel):
    value: str
    label: str

    class Config:
        orm_mode = True


class CascadeFilterProps(BaseModel):
    table_name: str
    col_name: str
    parent_name: str | None
    parent_values: list[str | None] | None
    search: str | None

    class Config:
        schema_extra = {
            "example": {
                "col_name": "DEF_CAUS_NAME_LV2",
                "parent_name": "DEF_CAUS_NAME_LV1",
                "parent_values": ["PCBA", "NDF"],
                "search": "Defect",
            }
        }


class RepairFilter(BaseModel):
    value: str | None

    class Config:
        orm_mode = True


# class freqType(str, Enum):
#     DAY = "DAY"
#     ISOWEEK = "WEEK"
#     MONTH = "MONTH"
#     YEAR = "YEAR"

class Frequency(str, Enum):
    DAY = "DAY"
    ISOWEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"

class ProcessFilters(BaseModel):
    PROD_CORP: list[str] = []
    PCSGNAME: list[str] = []
    PRODUCT_DIVIDE2: list[str] = []
    HQORG_ID: list[str] = []
    TOOL6: list[str] = []
    DEF_CAUS_NAME_LV1: list[str] = []
    DEF_CAUS_NAME_LV2: list[str] = []
    DEF_CAUS_NAME_LV3: list[str] = []
    DEF_SYM_NAME_1: list[str] = []  # Symptom code 추가
    DEF_SYM_NAME_2: list[str] = []
    DEF_SYM_NAME_3: list[str] = []


class ProcessDefectRateProps(ProcessFilters):
    column: str
    # date: datetime.date
    targetDate: datetime.date
    improve_rate: int
    
class ProcessDefectRateSSIProps(ProcessFilters):
    column: str
    # group: str ##추가시 process-quality/chart-ssi 실행 안됨
    date: datetime.date
    # targetDate: datetime.date
    # freqType: str ##추가시 process-quality/chart-ssi 실행 안됨
    # freqType: freqType #추가시 process-quality/chart-ssi 실행 안됨
    improve_rate: int

class ProcessSignalProps(ProcessFilters):
    column: str
    group: str


class ProcessDefectRateDetailProps(ProcessFilters):
    column: str
    group: str
    date: datetime.date
    freqType: str


class ProcessDefectRateDetailSSIProps(ProcessFilters):
    column: str
    group: str
    date: datetime.date
    freqType: str


class ProcessWarningProps(ProcessFilters):
    column: str
    group: str
    freqType: str
    targetDate: datetime.date


class ProcessCauseProps(ProcessFilters):
    column: str
    group: str
    target_date: datetime.date
    # targetDate: datetime.date
    freqType: Frequency
    

class ProcessSymptomProps(ProcessFilters):  # Symptom
    column: str
    group: str
    target_date: datetime.date
    # date: datetime.date   ### monthly도 연결 안됨
    # freqType: freqType
    freqType: Frequency

class ProcessDataProps(ProcessCauseProps):
    table_name: str

class ProcessDetailProps(ProcessCauseProps):
    is_compare: bool
    code: str


class ProcessData_sProps(ProcessSymptomProps):
    table_name: str
    
class ProcessDetail_sProps(ProcessSymptomProps):  # Symptom
    is_compare: bool
    code: str

class PartsReturnFilters(BaseModel):
    PROD_CORP: list[str] = []
    PCSGNAME: list[str] = []
    PRODUCT_DIVIDE2: list[str] = []
    HQORG_ID: list[str] = []
    TOOL6: list[str] = []
    PART_DESC: list[str] = []
    SUPPLIER_NAME: list[str] = []
    PART_NO: list[str] = []


class PartsReturnDefectRateProps(PartsReturnFilters):
    column: str
    date: datetime.date


class PartsReturnCauseProps(PartsReturnFilters):
    column: str
    group: str
    target_date: datetime.date
    # freqType: freqType
    freqType: Frequency


class PartsReturnDetailProps(PartsReturnCauseProps):
    is_compare: bool
    code: str


class FilterClause(BaseModel):
    prod_clause: str
    repair_clause: str
    params: dict


class QualityDataFilterOptions(dict):
    PRODUCT_DIVIDE1: list[str] | None
    PRODUCT_DIVIDE2: list[str] | None
    TOOL6: list[str] | None
    INCH: list[str] | None
    TOOL4: list[str] | None
    ATTRIBUTE6: list[str] | None
    DEV_YEAR: list[str] | None
    ADAPTER: list[str] | None
    GMES_OBM_OCM: list[str] | None
    GMES_MODULE_MAKER: list[str] | None
    GMES_MODULE_PROD_SITE: list[str] | None
    GMES_MODULE_REPAIR: list[str] | None
    GMES_PANEL_MAKER: list[str] | None
    GMES_PANEL_PROD_SITE: list[str] | None
    CONTINENT: list[str] | None
    SALES_CORP: list[str] | None
    PROD_CORP: list[str] | None
    SET_ID: list[str] | None
    LEVEL1: list[str] | None
    LEVEL1_KR_ORIG: list[str] | None
    PARTS_DESC1: list[str] | None
    LEVEL0: list[str] | None
    LEVEL2_SUMMARY: list[str] | None
    LEVEL2: list[str] | None
    LEVEL2_KR_ORIG: list[str] | None


class RawQueryParams(BaseModel):
    title: str
    sql: str


class QualityDataProps(BaseModel):
    title: str
    columnName: list[str]
    startDate: datetime.date
    endDate: datetime.date
    lookupType: str
    lookupFile: list[dict] = []
    filterOptions: QualityDataFilterOptions


class QualityDataResponse(BaseModel):
    id: int
    title: str
    file_path: str | None
    file_size: int | None
    file_length: int | None
    status: str | None
    remarks: str | None
    created_time: datetime.datetime | None
    complated_time: datetime.datetime | None
    created_by: str | None
    created_by_name: str | None

    class Config:
        orm_mode = True


class ProcessTrackerAll(QualityDataResponse):
    title: str
    column_name: str
    start_date: datetime.date
    end_date: datetime.date
    PRODUCT_DIVIDE1: str
    PRODUCT_DIVIDE2: str
    MODEL_SUFFIX: str | None
    TOOL6: str
    INCH: str
    TOOL4: str
    ATTRIBUTE6: str
    DEV_YEAR: str
    ADAPTER: str
    GMES_OBM_OCM: str
    GMES_MODULE_MAKER: str
    GMES_MODULE_PROD_SITE: str
    GMES_MODULE_REPAIR: str
    GMES_PANEL_MAKER: str
    GMES_PANEL_PROD_SITE: str
    CONTINENT: str
    SALES_CORP: str
    PROD_CORP: str
    SET_ID: str | None
    GMES_MODULE_ID: str | None
    GMES_PANEL_ID: str | None
    LEVEL1: str | None
    LEVEL1_KR_ORIG: str | None
    PARTS_DESC1: str | None
    LEVEL0: str | None
    LEVEL2_SUMMARY: str | None
    LEVEL2: str | None
    LEVEL2_KR_ORIG: str | None

    class Config:
        orm_mode = True


class ProcessCause(BaseModel):
    index: int
    DEF_CAUS_CODE: str
    DEF_CAUS_NAME_LV1: str
    DEF_CAUS_NAME_LV2: str
    DEF_CAUS_NAME_LV3: str
    DEF_QTY: int
    P1_DEF_QTY: int
    P2_DEF_QTY: int
    PROD_QTY: int
    P1_PROD_QTY: int
    P2_PROD_QTY: int
    RATE: float
    P1_RATE: float
    P2_RATE: float

class ProcessSymptom(BaseModel):  # JS 1004 추가 HA Symptom
    index: int
    DEF_SYM_CODE: str
    DEF_SYM_NAME_1: str
    DEF_SYM_NAME_2: str
    DEF_SYM_NAME_3: str
    DEF_QTY: int
    P1_DEF_QTY: int
    P2_DEF_QTY: int
    PROD_QTY: int
    P1_PROD_QTY: int
    P2_PROD_QTY: int
    RATE: float
    P1_RATE: float
    P2_RATE: float

class ReturnCause(BaseModel):
    index: int
    PART_DESC: str | None
    SUPPLIER_NAME: str | None
    PART_NO: str | None
    DEF_QTY: int
    P1_DEF_QTY: int
    P2_DEF_QTY: int
    PROD_QTY: int
    P1_PROD_QTY: int
    P2_PROD_QTY: int
    RATE: float
    P1_RATE: float
    P2_RATE: float


class GetUserInfo(BaseOrmModel):
    username: str
    employee_number: int | None
    name: str
    en_name: str | None
    title: str
    department: str
    email: str
    full_name: str


class GetUserDetail(GetUserInfo):
    assigned_count: int | None
    approval_count: int | None
    managing_count: int | None
    count_all: int


class GetMailing(BaseOrmModel):
    to: list[GetUserInfo] = []
    cc: list[GetUserInfo] = []


class Solution(BaseOrmModel):
    manager: GetUserInfo
    mailing: GetMailing


class GetIssueTrackerHistory(BaseOrmModel):
    id: int
    history_type: str
    note: str | None
    created_at: datetime.datetime
    author: GetUserInfo = {}


class GetIssueTrackerComment(BaseOrmModel):
    comment_type: str


class GetIssueTrackerFiles(BaseOrmModel):
    id: int
    name: str
    status: str
    file_path: str
    file_type: str
    file_size: int
    created_by: str
    created_at: datetime.datetime
    last_modified_at: datetime.datetime


class GetIssueTrackerCommentWithReply(GetIssueTrackerComment):
    id: int
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    author: GetUserInfo
    parent_id: int | None
    replies: list[GetIssueTrackerCommentWithReply] = []
    files: list[GetIssueTrackerFiles] = []


class GetIssueTracker(BaseOrmModel):
    id: int
    category: str
    prod_corp: str
    status: str
    priority: str
    subject: str
    label: str | None
    keywords: str | None
    due_date: datetime.date | None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    author: GetUserInfo
    assignee: GetUserInfo | None
    to: list[GetUserInfo] = []
    cc: list[GetUserInfo] = []
    comments_count: int


class GetIssueTrackerWithChildren(GetIssueTracker):
    content: str | None
    solution: Solution
    files: list[GetIssueTrackerFiles] = []
    history: list[GetIssueTrackerHistory] = []
    comments: list[GetIssueTrackerCommentWithReply] = []


class CreateIssueTracker(BaseModel):
    category: str
    prod_corp: str
    priority: str
    label: str | None
    keywords: str | None
    subject: str
    content: str | None
    due_date: datetime.date | None
    to: list[str] = []
    cc: list[str] = []
    files: list[dict] = []


class CreateIssueTrackerComment(BaseModel):
    comment_type: str
    content: str
    assignee_id: str | None
    to: list[str] = []
    cc: list[str] = []
    files: list[dict] = []


class UpdateIssueTrackerComment(BaseModel):
    content: str


class CreateIssueTrackerEvent(CreateIssueTracker):
    tracker_id: int
    event_type: str
    note: str
    author: str
