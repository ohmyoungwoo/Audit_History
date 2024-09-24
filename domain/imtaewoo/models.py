from sqlalchemy import (
    Column,
    UniqueConstraint,
    sql,
    ForeignKey,
    String,
    Integer,
    Float,
    Date,
    DateTime,
    Text,
    Boolean,
    Table,
)
from sqlalchemy.orm import with_loader_criteria
from sqlalchemy import event
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from app.database import Base, SessionLocal


class Audit(Base):
    __tablename__ = "audit_record"

    id = Column(Integer, primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date)
    org_name = Column(String(50))
    vendor_code = Column(String(50))
    vendor_name = Column(String(50))
    division_name = Column(String(50))
    category_code = Column(String(50))
    part_name = Column(String(50))
    audit_type = Column(String(50))
    phases = Column(Integer)
    manager_name = Column(String(100))
    common_score = Column(Float)
    expertise_score = Column(Float)
    total_score = Column(Float)
    grade = Column(String(50))
    orig_file_name = Column(String(100))
    file_size = Column(Integer)
    file_path = Column(String(200))
    created_date = Column(DateTime, default=sql.func.now())
    created_by = Column(String(50))
    modified_date = Column(DateTime)
    modified_by = Column(String(50))

    common_detail = relationship(
        "AuditCommonScore", backref="parent", passive_deletes=True
    )

    expertise_detail = relationship(
        "AuditExpertiseScore", backref="parent", passive_deletes=True
    )

    countermeasure = relationship(
        "AuditCountermeasure", backref="parent", passive_deletes=True
    )


class AuditCommonScore(Base):
    __tablename__ = "audit_common_score"

    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    item = Column(String(50))
    score = Column(Float)
    created_date = Column(DateTime, default=sql.func.now())
    created_by = Column(String(50))
    record_id = Column(Integer, ForeignKey("audit_record.id", ondelete="CASCADE"))


class AuditExpertiseScore(Base):
    __tablename__ = "audit_expertise_score"

    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    item = Column(String(50))
    score = Column(Float)
    created_date = Column(DateTime, default=sql.func.now())
    created_by = Column(String(50))
    record_id = Column(Integer, ForeignKey("audit_record.id", ondelete="CASCADE"))


class AuditCountermeasure(Base):
    __tablename__ = "audit_countermeasure"

    id = Column(Integer, primary_key=True)
    item = Column(String(200))
    points = Column(Text, index=False)
    measures = Column(Text, index=False)
    completion_date = Column(DateTime)
    review_result = Column(Text, index=False)
    status = Column(String(50))
    importance = Column(String(50))
    record_id = Column(Integer, ForeignKey("audit_record.id", ondelete="CASCADE"))


class AuditSchedule(Base):
    __tablename__ = "audit_schedule"

    id = Column(Integer, primary_key=True)
    org_name = Column(String(50))
    vendor_code = Column(String(50))
    scheduled_date = Column(Date)
    created_date = Column(DateTime, default=sql.func.now())
    created_by = Column(String(50))
    modified_date = Column(DateTime)
    modified_by = Column(String(50))


class Penalty(Base):
    __tablename__ = "penalty_history"

    id = Column(Integer, primary_key=True)
    issue_date = Column(Date)
    penalty_date = Column(Date)  
    heqm_code = Column(String(20))
    document_type = Column(String(50))
    reason_code = Column(String(50))
    division_name = Column(String(50))
    category_code = Column(String(50))
    vendor_code = Column(String(50))
    vendor_name = Column(String(50))
    part_name = Column(String(50))
    manager_name = Column(String(50))
    contents = Column(String(100))
    status = Column(String(50))
    created_date = Column(DateTime, default=sql.func.now())
    created_by = Column(String(50))
    modified_date = Column(DateTime)
    modified_by = Column(String(50))
    files = relationship("PenaltyAttach", backref="parent", passive_deletes=True)


class PenaltyAttach(Base):
    __tablename__ = "penalty_attach"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    status = Column(String(50))
    file_path = Column(String(200))
    file_type = Column(String(100))
    file_size = Column(Integer)
    created_by = Column(String(50))
    created_date = Column(DateTime, default=sql.func.now())
    last_modified_date = Column(DateTime)
    history_id = Column(Integer, ForeignKey("penalty_history.id", ondelete="CASCADE"))


class Vendor(Base):
    __tablename__ = "vendor_name"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=sql.func.now())
    vendor_code = Column(String(20))
    vendor_name = Column(String(50))
    writer = Column(String(50))


class PresetResult(Base):
    __tablename__ = "PRESET_LIST_RESULT"

    IDX = Column(mysql.INTEGER(255), primary_key=True)
    PRESET_IDX = Column(mysql.INTEGER(255))
    PRESET_SIGNAL = Column(mysql.VARCHAR(255))
    PRESET_RESULT = Column(mysql.LONGTEXT)
    PRESET_IMAGE = Column(mysql.LONGTEXT)
    PRESET_LOG = Column(mysql.DATETIME(fsp=6), default=sql.func.now())


class PresetOperate(Base):
    __tablename__ = "PRESET_LIST_OPERATE"

    IDX = Column(mysql.INTEGER(11), primary_key=True)
    PRESET_TYPE = Column(mysql.VARCHAR(255))
    PRESET_PRODUCT = Column(mysql.VARCHAR(255))
    PRESET_ANALYSIS = Column(mysql.VARCHAR(255))
    PRESET_AUTODATE = Column(mysql.VARCHAR(255))
    PRESET_BASEDATE = Column(mysql.VARCHAR(255))
    PRESET_TITLE = Column(mysql.VARCHAR(255))
    PRESET_DESC = Column(mysql.LONGTEXT)
    PRESET_FOOTNOTE = Column(mysql.LONGTEXT)
    PRESET_CHART = Column(mysql.LONGTEXT)
    PRESET_OPTIONS = Column(mysql.LONGTEXT)
    PRESET_FILTERS = Column(mysql.LONGTEXT)
    PRESET_CRITERIA = Column(mysql.LONGTEXT)
    REPORT_FREQ = Column(mysql.VARCHAR(255))
    REPORT_DAYS = Column(mysql.VARCHAR(255))
    REPORT_TIME = Column(mysql.VARCHAR(255))
    REPORT_TO = Column(mysql.VARCHAR(1024))
    REPORT_CC = Column(mysql.VARCHAR(1024))
    PRESET_REGISTRANT = Column(mysql.VARCHAR(255))
    PRESET_CREATED = Column(mysql.DATETIME(fsp=6), default=sql.func.now())
    PRESET_MODIFIED = Column(mysql.DATETIME(fsp=6))
    PRESET_STATUS = Column(mysql.VARCHAR(255))


class UHDPanelDashboard(Base):
    __tablename__ = "DASHBOARD_UHD_PANEL_MAKER"

    IDX = Column(mysql.BIGINT(20), primary_key=True)
    GMES_PANEL_MAKER = Column(mysql.TEXT)
    PROD_CORP = Column(mysql.TEXT)
    INCH = Column(mysql.TEXT)
    PROD_QTY = Column(mysql.BIGINT(20))
    SVC_QTY = Column(mysql.BIGINT(20))
    Y_2 = Column(mysql.DOUBLE)
    Y_1 = Column(mysql.DOUBLE)
    Y_0 = Column(mysql.DOUBLE)
    M_2 = Column(mysql.DOUBLE)
    M_1 = Column(mysql.DOUBLE)
    M_0 = Column(mysql.DOUBLE)
    YoY = Column(mysql.TEXT)
    MoM = Column(mysql.TEXT)
    DASHBOARD_COLUMNS_NAME = Column(mysql.TEXT)
    FIXED_FDR_PRESET_IDX = Column(mysql.DOUBLE)
    FIXED_FDR_PRESET_TITLE = Column(mysql.TEXT)
    FIXED_FDR_PRESET_CHART = Column(mysql.TEXT)
    FIXED_FDR_PRESET_OPTION = Column(mysql.TEXT)
    FIXED_FDR_PRESET_FILTER = Column(mysql.TEXT)
    FIXED_FDR_CHART = Column(mysql.TEXT)
    FIXED_FDR_TABLE = Column(mysql.TEXT)
    FIXED_FDR_HEADER = Column(mysql.TEXT)
    FIXED_FDR_GROUP = Column(mysql.TEXT)
    FIXED_LEVEL2_TABLE = Column(mysql.TEXT)
    PASSED_FDR_PRESET_IDX = Column(mysql.DOUBLE)
    PASSED_FDR_PRESET_TITLE = Column(mysql.TEXT)
    PASSED_FDR_PRESET_CHART = Column(mysql.TEXT)
    PASSED_FDR_PRESET_OPTION = Column(mysql.TEXT)
    PASSED_FDR_PRESET_FILTER = Column(mysql.TEXT)
    PASSED_FDR_CHART = Column(mysql.TEXT)
    PASSED_FDR_TABLE = Column(mysql.TEXT)
    PASSED_LEVEL2_TABLE = Column(mysql.TEXT)
    PASSED_LEVEL2_GROUP = Column(mysql.TEXT)
    HAZARD_PRESET_IDX = Column(mysql.DOUBLE)
    HAZARD_PRESET_TITLE = Column(mysql.TEXT)
    HAZARD_PRESET_CHART = Column(mysql.TEXT)
    HAZARD_PRESET_OPTION = Column(mysql.TEXT)
    HAZARD_PRESET_FILTER = Column(mysql.TEXT)
    HAZARD_CHART = Column(mysql.TEXT)
    HAZARD_TABLE = Column(mysql.TEXT)
    HAZARD_GROUP = Column(mysql.TEXT)


class OLEDModuleDashboard(Base):
    __tablename__ = "DASHBOARD_OLED_MODULE_PROD_SITE"

    IDX = Column(mysql.BIGINT(20), primary_key=True)
    GMES_MODULE_PROD_SITE = Column(mysql.TEXT)
    GMES_PANEL_PROD_SITE = Column(mysql.TEXT)
    PROD_CORP = Column(mysql.TEXT)
    INCH = Column(mysql.TEXT)
    PROD_QTY = Column(mysql.BIGINT(20))
    SVC_QTY = Column(mysql.BIGINT(20))
    Y_2 = Column(mysql.DOUBLE)
    Y_1 = Column(mysql.DOUBLE)
    Y_0 = Column(mysql.DOUBLE)
    M_2 = Column(mysql.DOUBLE)
    M_1 = Column(mysql.DOUBLE)
    M_0 = Column(mysql.DOUBLE)
    YoY = Column(mysql.TEXT)
    MoM = Column(mysql.TEXT)
    DASHBOARD_COLUMNS_NAME = Column(mysql.TEXT)
    FIXED_FDR_PRESET_IDX = Column(mysql.DOUBLE)
    FIXED_FDR_PRESET_TITLE = Column(mysql.TEXT)
    FIXED_FDR_PRESET_CHART = Column(mysql.TEXT)
    FIXED_FDR_PRESET_OPTION = Column(mysql.TEXT)
    FIXED_FDR_PRESET_FILTER = Column(mysql.TEXT)
    FIXED_FDR_CHART = Column(mysql.TEXT)
    FIXED_FDR_TABLE = Column(mysql.TEXT)
    FIXED_FDR_HEADER = Column(mysql.TEXT)
    FIXED_FDR_GROUP = Column(mysql.TEXT)
    FIXED_LEVEL2_TABLE = Column(mysql.TEXT)
    PASSED_FDR_PRESET_IDX = Column(mysql.DOUBLE)
    PASSED_FDR_PRESET_TITLE = Column(mysql.TEXT)
    PASSED_FDR_PRESET_CHART = Column(mysql.TEXT)
    PASSED_FDR_PRESET_OPTION = Column(mysql.TEXT)
    PASSED_FDR_PRESET_FILTER = Column(mysql.TEXT)
    PASSED_FDR_CHART = Column(mysql.TEXT)
    PASSED_FDR_TABLE = Column(mysql.TEXT)
    PASSED_LEVEL2_TABLE = Column(mysql.TEXT)
    PASSED_LEVEL2_GROUP = Column(mysql.TEXT)
    HAZARD_PRESET_IDX = Column(mysql.DOUBLE)
    HAZARD_PRESET_TITLE = Column(mysql.TEXT)
    HAZARD_PRESET_CHART = Column(mysql.TEXT)
    HAZARD_PRESET_OPTION = Column(mysql.TEXT)
    HAZARD_PRESET_FILTER = Column(mysql.TEXT)
    HAZARD_CHART = Column(mysql.TEXT)
    HAZARD_TABLE = Column(mysql.TEXT)
    HAZARD_GROUP = Column(mysql.TEXT)


class PSUDashboard(Base):
    __tablename__ = "DASHBOARD_PSU_MAKER"

    IDX = Column(mysql.BIGINT(20), primary_key=True)
    PRODUCT_DIVIDE1 = Column(mysql.TEXT)
    GMES_PSU_MAKER = Column(mysql.TEXT)
    PROD_CORP = Column(mysql.TEXT)
    PROD_QTY = Column(mysql.BIGINT(20))
    SVC_QTY = Column(mysql.BIGINT(20))
    Y_2 = Column(mysql.DOUBLE)
    Y_1 = Column(mysql.DOUBLE)
    Y_0 = Column(mysql.DOUBLE)
    M_2 = Column(mysql.DOUBLE)
    M_1 = Column(mysql.DOUBLE)
    M_0 = Column(mysql.DOUBLE)
    YoY = Column(mysql.TEXT)
    MoM = Column(mysql.TEXT)
    DASHBOARD_COLUMNS_NAME = Column(mysql.TEXT)
    FIXED_FDR_PRESET_IDX = Column(mysql.DOUBLE)
    FIXED_FDR_PRESET_TITLE = Column(mysql.TEXT)
    FIXED_FDR_PRESET_CHART = Column(mysql.TEXT)
    FIXED_FDR_PRESET_OPTION = Column(mysql.TEXT)
    FIXED_FDR_PRESET_FILTER = Column(mysql.TEXT)
    FIXED_FDR_CHART = Column(mysql.TEXT)
    FIXED_FDR_TABLE = Column(mysql.TEXT)
    FIXED_FDR_HEADER = Column(mysql.TEXT)
    FIXED_FDR_GROUP = Column(mysql.TEXT)
    FIXED_LEVEL2_TABLE = Column(mysql.TEXT)
    PASSED_FDR_PRESET_IDX = Column(mysql.DOUBLE)
    PASSED_FDR_PRESET_TITLE = Column(mysql.TEXT)
    PASSED_FDR_PRESET_CHART = Column(mysql.TEXT)
    PASSED_FDR_PRESET_OPTION = Column(mysql.TEXT)
    PASSED_FDR_PRESET_FILTER = Column(mysql.TEXT)
    PASSED_FDR_CHART = Column(mysql.TEXT)
    PASSED_FDR_TABLE = Column(mysql.TEXT)
    PASSED_LEVEL2_TABLE = Column(mysql.TEXT)
    PASSED_LEVEL2_GROUP = Column(mysql.TEXT)
    HAZARD_PRESET_IDX = Column(mysql.DOUBLE)
    HAZARD_PRESET_TITLE = Column(mysql.TEXT)
    HAZARD_PRESET_CHART = Column(mysql.TEXT)
    HAZARD_PRESET_OPTION = Column(mysql.TEXT)
    HAZARD_PRESET_FILTER = Column(mysql.TEXT)
    HAZARD_CHART = Column(mysql.TEXT)
    HAZARD_TABLE = Column(mysql.TEXT)
    HAZARD_GROUP = Column(mysql.TEXT)


class RemoteDashboard(Base):
    __tablename__ = "DASHBOARD_REMOTE_MAKER"

    IDX = Column(mysql.BIGINT(20), primary_key=True)
    PRODUCT_DIVIDE1 = Column(mysql.TEXT)
    GMES_REMOCON_MAKER = Column(mysql.TEXT)
    PROD_CORP = Column(mysql.TEXT)
    PROD_QTY = Column(mysql.BIGINT(20))
    SVC_QTY = Column(mysql.BIGINT(20))
    Y_2 = Column(mysql.DOUBLE)
    Y_1 = Column(mysql.DOUBLE)
    Y_0 = Column(mysql.DOUBLE)
    M_2 = Column(mysql.DOUBLE)
    M_1 = Column(mysql.DOUBLE)
    M_0 = Column(mysql.DOUBLE)
    YoY = Column(mysql.TEXT)
    MoM = Column(mysql.TEXT)
    DASHBOARD_COLUMNS_NAME = Column(mysql.TEXT)
    FIXED_FDR_PRESET_IDX = Column(mysql.DOUBLE)
    FIXED_FDR_PRESET_TITLE = Column(mysql.TEXT)
    FIXED_FDR_PRESET_CHART = Column(mysql.TEXT)
    FIXED_FDR_PRESET_OPTION = Column(mysql.TEXT)
    FIXED_FDR_PRESET_FILTER = Column(mysql.TEXT)
    FIXED_FDR_CHART = Column(mysql.TEXT)
    FIXED_FDR_TABLE = Column(mysql.TEXT)
    FIXED_FDR_HEADER = Column(mysql.TEXT)
    FIXED_FDR_GROUP = Column(mysql.TEXT)
    FIXED_LEVEL2_TABLE = Column(mysql.TEXT)
    PASSED_FDR_PRESET_IDX = Column(mysql.DOUBLE)
    PASSED_FDR_PRESET_TITLE = Column(mysql.TEXT)
    PASSED_FDR_PRESET_CHART = Column(mysql.TEXT)
    PASSED_FDR_PRESET_OPTION = Column(mysql.TEXT)
    PASSED_FDR_PRESET_FILTER = Column(mysql.TEXT)
    PASSED_FDR_CHART = Column(mysql.TEXT)
    PASSED_FDR_TABLE = Column(mysql.TEXT)
    PASSED_LEVEL2_TABLE = Column(mysql.TEXT)
    PASSED_LEVEL2_GROUP = Column(mysql.TEXT)
    HAZARD_PRESET_IDX = Column(mysql.DOUBLE)
    HAZARD_PRESET_TITLE = Column(mysql.TEXT)
    HAZARD_PRESET_CHART = Column(mysql.TEXT)
    HAZARD_PRESET_OPTION = Column(mysql.TEXT)
    HAZARD_PRESET_FILTER = Column(mysql.TEXT)
    HAZARD_CHART = Column(mysql.TEXT)
    HAZARD_TABLE = Column(mysql.TEXT)
    HAZARD_GROUP = Column(mysql.TEXT)


class SalesCorpModelDashboard(Base):
    __tablename__ = "DASHBOARD_MODEL_BY_SALES_CORP"

    IDX = Column(mysql.BIGINT(20), primary_key=True)
    CONTINENT = Column(mysql.TEXT)
    SALES_CORP = Column(mysql.TEXT)
    PROD_GROUP = Column(mysql.TEXT)
    MODEL_GROUP = Column(mysql.TEXT)
    BASE_GROUP = Column(mysql.TEXT)
    PASSED_MON = Column(mysql.TEXT)
    TF_SALES = Column(mysql.TEXT)
    TF_SVC = Column(mysql.TEXT)
    BF_SALES = Column(mysql.TEXT)
    BF_SVC = Column(mysql.TEXT)
    BASE_GROUP_NUM = Column(mysql.BIGINT(20))
    DEV_YEAR = Column(mysql.BIGINT(20))
    PRODUCT_DIVIDE1 = Column(mysql.TEXT)
    ATTRIBUTE6 = Column(mysql.TEXT)
    INCH = Column(mysql.TEXT)
    TOOL4 = Column(mysql.TEXT)
    PASSED_MON_NUM = Column(mysql.BIGINT(20))
    MODEL_FDR_M0 = Column(mysql.DOUBLE)
    MODEL_ACC_SVC_M0 = Column(mysql.DOUBLE)
    MODEL_ACC_SALES_M0 = Column(mysql.DOUBLE)
    MODEL_MOM_SALES_M0 = Column(mysql.DOUBLE)
    BASE_FDR = Column(mysql.DOUBLE)
    BASE_ACC_SVC = Column(mysql.DOUBLE)
    BASE_ACC_SALES = Column(mysql.DOUBLE)
    MODEL_FDR_M1 = Column(mysql.DOUBLE)
    MODEL_ACC_SVC_M1 = Column(mysql.DOUBLE)
    MODEL_ACC_SALES_M1 = Column(mysql.DOUBLE)
    MODEL_MOM_SALES_M1 = Column(mysql.DOUBLE)
    MODEL_FDR_M2 = Column(mysql.DOUBLE)
    MODEL_ACC_SVC_M2 = Column(mysql.DOUBLE)
    MODEL_ACC_SALES_M2 = Column(mysql.DOUBLE)
    MODEL_MOM_SALES_M2 = Column(mysql.DOUBLE)
    YoY = Column(mysql.DOUBLE)
    MoM_M1 = Column(mysql.DOUBLE)
    MoM_M2 = Column(mysql.DOUBLE)
    EXCEPT = Column(mysql.TEXT)
    EXCEPT_DESC = Column(mysql.TEXT)
    PASSED_FDR_PRESET_IDX = Column(mysql.BIGINT(20))
    PASSED_FDR_PRESET_TITLE = Column(mysql.TEXT)
    PASSED_FDR_PRESET_CHART = Column(mysql.TEXT)
    PASSED_FDR_PRESET_OPTION = Column(mysql.TEXT)
    PASSED_FDR_PRESET_FILTER = Column(mysql.TEXT)
    PASSED_FDR_CHART = Column(mysql.TEXT)
    PASSED_FDR_TABLE = Column(mysql.TEXT)
    PASSED_LEVEL1_TABLE = Column(mysql.TEXT)
    PASSED_LEVEL1_GROUP = Column(mysql.TEXT)
    PASSED_LEVEL2_TABLE = Column(mysql.TEXT)
    PASSED_LEVEL2_GROUP = Column(mysql.TEXT)
    HAZARD_PRESET_IDX = Column(mysql.BIGINT(20))
    HAZARD_PRESET_TITLE = Column(mysql.TEXT)
    HAZARD_PRESET_CHART = Column(mysql.TEXT)
    HAZARD_PRESET_OPTION = Column(mysql.TEXT)
    HAZARD_PRESET_FILTER = Column(mysql.TEXT)
    HAZARD_CHART = Column(mysql.TEXT)
    HAZARD_TABLE = Column(mysql.TEXT)
    HAZARD_GROUP = Column(mysql.TEXT)


class SalesDashboardIssue(Base):
    __tablename__ = "sales_dashboard_issue"

    id = Column(String(15), primary_key=True)
    detail = Column(mysql.TEXT)
    modified_date = Column(DateTime)
    modified_by = Column(String(50))
    created_date = Column(DateTime, default=sql.func.now())
    created_by = Column(String(50))


class PresetChart(Base):
    __tablename__ = "preset_chart"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=sql.func.now())
    preset_id = Column(Integer)
    options = Column(mysql.LONGTEXT)


class PresetTable(Base):
    __tablename__ = "preset_table"

    id = Column(mysql.DOUBLE, primary_key=True)
    product = Column(mysql.TEXT)
    region = Column(mysql.TEXT)
    parts = Column(mysql.TEXT)
    report_idx = Column(mysql.DOUBLE)
    hazard_idx = Column(mysql.DOUBLE)
    yoy = Column(mysql.TEXT)
    before2month = Column(mysql.TEXT)
    before1month = Column(mysql.TEXT)
    thismonth = Column(mysql.TEXT)
    ffr_recommend = Column(mysql.TEXT)
    hzd_recommend = Column(mysql.TEXT)
    target = Column(mysql.TEXT)
    signal = Column(mysql.TEXT)


class PresetTableODM(Base):
    __tablename__ = "preset_odm_table"

    id = Column(mysql.DOUBLE, primary_key=True)
    product = Column(mysql.TEXT)
    vendor = Column(mysql.TEXT)
    parts = Column(mysql.TEXT)
    report_idx = Column(mysql.DOUBLE)
    hazard_idx = Column(mysql.DOUBLE)
    yoy = Column(mysql.TEXT)
    before2month = Column(mysql.TEXT)
    before1month = Column(mysql.TEXT)
    thismonth = Column(mysql.TEXT)
    ffr_recommend = Column(mysql.TEXT)
    hzd_recommend = Column(mysql.TEXT)
    target = Column(mysql.TEXT)
    signal = Column(mysql.TEXT)


class PresetTableModel(Base):
    __tablename__ = "preset_model_table"

    ID = Column(mysql.DOUBLE, primary_key=True)
    PRESET_IDX = Column(mysql.DOUBLE)
    CONTINENT = Column(mysql.TEXT)
    SALES_CORP = Column(mysql.TEXT)
    PROD_GROUP = Column(mysql.TEXT)
    MODEL_GROUP = Column(mysql.TEXT)
    BASE_GROUP = Column(mysql.TEXT)
    PASSED_MON = Column(mysql.TEXT)
    MODEL_FDR_M0 = Column(mysql.TEXT)
    MODEL_ACC_SVC_M0 = Column(mysql.TEXT)
    MODEL_ACC_SALES_M0 = Column(mysql.TEXT)
    MODEL_MOM_SALES_M0 = Column(mysql.TEXT)
    BASE_FDR = Column(mysql.TEXT)
    BASE_ACC_SVC = Column(mysql.TEXT)
    BASE_ACC_SALES = Column(mysql.TEXT)
    MODEL_FDR_M1 = Column(mysql.TEXT)
    MODEL_ACC_SVC_M1 = Column(mysql.TEXT)
    MODEL_ACC_SALES_M1 = Column(mysql.TEXT)
    MODEL_MOM_SALES_M1 = Column(mysql.TEXT)
    MODEL_FDR_M2 = Column(mysql.TEXT)
    MODEL_ACC_SVC_M2 = Column(mysql.TEXT)
    MODEL_ACC_SALES_M2 = Column(mysql.TEXT)
    MODEL_MOM_SALES_M2 = Column(mysql.TEXT)
    YoY = Column(mysql.TEXT)
    MoM = Column(mysql.TEXT)
    EXCEPT = Column(mysql.TEXT)
    EXCEPT_DESC = Column(mysql.TEXT)


class PresetMeta(Base):
    __tablename__ = "ETL_METADATA_PRESET_LIST"

    TS_BEGIN = Column(mysql.TEXT, primary_key=True)
    TS_END = Column(mysql.TEXT)
    TV_MAX_DT_FFR_FDR_RPT = Column(mysql.TEXT)
    TV_MAX_DT_FFR = Column(mysql.TEXT)
    TV_MAX_DT_FDR = Column(mysql.TEXT)
    TV_MAX_DT_HAZARD = Column(mysql.TEXT)
    TV_MAX_DT_SVC_CNT = Column(mysql.TEXT)
    AV_MAX_DT_FFR_FDR_RPT = Column(mysql.TEXT)
    AV_MAX_DT_FFR = Column(mysql.TEXT)
    AV_MAX_DT_FDR = Column(mysql.TEXT)
    AV_MAX_DT_HAZARD = Column(mysql.TEXT)
    AV_MAX_DT_SVC_CNT = Column(mysql.TEXT)


class Filter(Base):
    __tablename__ = "TV_FILTER_BAS"

    index = Column(Integer, primary_key=True)
    COL_NAME = Column(String(100))
    CONTENTS = Column(String(100))


class FieldFilter(Base):
    __tablename__ = "field_tv_filter"

    index = Column(Integer, primary_key=True)
    PRODUCT_DIVIDE1 = Column(mysql.TEXT)
    PRODUCT_DIVIDE2 = Column(mysql.TEXT)
    TOOL6 = Column(mysql.TEXT)
    INCH = Column(mysql.TEXT)
    TOOL4 = Column(mysql.TEXT)
    ATTRIBUTE6 = Column(mysql.TEXT)
    DEV_YEAR = Column(mysql.TEXT)
    MAIN_SOC = Column(mysql.TEXT)
    ADAPTER = Column(mysql.TEXT)
    OS_DIVIDE = Column(mysql.TEXT)
    GMES_OBM_OCM = Column(mysql.TEXT)
    GMES_MODULE_MAKER = Column(mysql.TEXT)
    GMES_MODULE_PROD_SITE = Column(mysql.TEXT)
    GMES_MODULE_REPAIR = Column(mysql.TEXT)
    GMES_PANEL_MAKER = Column(mysql.TEXT)
    GMES_PANEL_PROD_SITE = Column(mysql.TEXT)
    CONTINENT = Column(mysql.TEXT)
    SALES_CORP = Column(mysql.TEXT)
    PROD_CORP = Column(mysql.TEXT)
    TABLE_NAME = Column(mysql.TEXT)


class CascadeFilter(Base):
    __tablename__ = "cascade_filter_base"

    index = Column(mysql.BIGINT, primary_key=True)
    table_name = Column(mysql.TEXT)
    parent_name = Column(mysql.TEXT)
    parent_value = Column(mysql.TEXT)
    col_name = Column(mysql.TEXT)
    value = Column(mysql.TEXT)


class QualityData(Base):
    __tablename__ = "tracking_history"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    column_name = Column(Text, index=False)
    lookup_type = Column(String(100))
    lookup_values = Column(mysql.LONGTEXT, index=False)
    filter_options = Column(mysql.LONGTEXT, index=False)
    file_path = Column(String(100), index=False)
    file_size = Column(mysql.INTEGER(20))
    file_length = Column(Integer)
    status = Column(String(50))
    remarks = Column(String(256))
    created_time = Column(DateTime, default=sql.func.now())
    complated_time = Column(DateTime)
    created_by = Column(String(50))
    created_by_name = Column(String(50))


class RawQuery(Base):
    __tablename__ = "raw_query_history"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    sql = Column(mysql.LONGTEXT, index=False)
    file_path = Column(String(100), index=False)
    file_size = Column(mysql.INTEGER(20))
    file_length = Column(Integer)
    status = Column(String(50))
    remarks = Column(String(200))
    created_time = Column(DateTime, default=datetime.now)
    complated_time = Column(DateTime)
    created_by = Column(String(50))
    created_by_name = Column(String(50))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(100))
    name = Column(String(50))
    en_name = Column(String(50))
    title = Column(String(50))
    employeeNumber = Column(String(50))
    department = Column(String(50))
    office = Column(String(50))
    mobile = Column(String(50))
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime)
    date_joined = Column(DateTime, default=sql.func.now())


default_mailing_to_association_table = Table(
    "default_mailing_to_association",
    Base.metadata,
    Column("user_id", ForeignKey("issue_tracker_user.username"), primary_key=True),
    Column("mailing_id", ForeignKey("issue_tracker_mailing.id"), primary_key=True),
)

default_mailing_cc_association_table = Table(
    "default_mailing_cc_association",
    Base.metadata,
    Column("user_id", ForeignKey("issue_tracker_user.username"), primary_key=True),
    Column("mailing_id", ForeignKey("issue_tracker_mailing.id"), primary_key=True),
)

issue_mailing_to_association_table = Table(
    "issue_mailing_to_association",
    Base.metadata,
    Column("user_id", ForeignKey("issue_tracker_user.username"), primary_key=True),
    Column("issue_id", ForeignKey("issue_tracker.id"), primary_key=True),
)

issue_mailing_cc_association_table = Table(
    "issue_mailing_cc_association",
    Base.metadata,
    Column("user_id", ForeignKey("issue_tracker_user.username"), primary_key=True),
    Column("issue_id", ForeignKey("issue_tracker.id"), primary_key=True),
)


class IssueTracker(Base):
    __tablename__ = "issue_tracker"

    id = Column(Integer, primary_key=True)
    category = Column(String(50))
    prod_corp = Column(String(50))
    status = Column(String(50))
    priority = Column(String(50))
    label = Column(String(50))
    keywords = Column(String(50))
    subject = Column(String(50))
    content = Column(mysql.LONGTEXT, index=False)
    due_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    closed_at = Column(DateTime)
    solution_id = Column(Integer, ForeignKey("issue_tracker_solution.id"))
    author_id = Column(String(50), ForeignKey("issue_tracker_user.username"))
    assignee_id = Column(String(50), ForeignKey("issue_tracker_user.username"))
    author = relationship(
        "IssueTrackerUser", foreign_keys=[author_id], backref="issues"
    )
    assignee = relationship(
        "IssueTrackerUser", foreign_keys=[assignee_id], backref="assigned_issues"
    )
    history = relationship("IssueTrackerHistory", backref="issue")
    comments = relationship("IssueTrackerComment", backref="issue")
    files = relationship("IssueTrackerFiles", backref="issue_tracker")
    to = relationship(
        "IssueTrackerUser",
        secondary=issue_mailing_to_association_table,
        backref="issue_to",
    )
    cc = relationship(
        "IssueTrackerUser",
        secondary=issue_mailing_cc_association_table,
        backref="issue_cc",
    )
    is_delete = Column(Boolean, default=False)

    @hybrid_property
    def comments_count(self):
        return len(self.comments)


@event.listens_for(SessionLocal, "do_orm_execute")
def _do_orm_execute(orm_execute_state):
    if (
        orm_execute_state.is_select
        and not orm_execute_state.is_column_load
        and not orm_execute_state.is_relationship_load
    ):
        orm_execute_state.statement = orm_execute_state.statement.options(
            with_loader_criteria(IssueTracker, IssueTracker.is_delete == False)
        )


class IssueTrackerUser(Base):
    __tablename__ = "issue_tracker_user"

    username = Column(String(50), primary_key=True)
    employee_number = Column(String(10))
    name = Column(String(50))
    en_name = Column(String(50))
    title = Column(String(50))
    department = Column(String(50))
    email = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    history = relationship("IssueTrackerHistory", backref="author")
    comments = relationship("IssueTrackerComment", backref="author")

    @hybrid_property
    def assigned_count(self):
        return len(list(filter(lambda x: x.status != "closed", self.assigned_issues)))

    @hybrid_property
    def approval_count(self):
        return len(list(filter(lambda x: x.status == "fixed", self.issues)))

    @hybrid_property
    def managing_count(self):
        issue_count = 0
        solutions = self.manage_solution
        for solution in solutions:
            issue_count += len(
                list(filter(lambda x: x.status != "closed", solution.issues))
            )
        return issue_count

    @hybrid_property
    def count_all(self):
        return self.assigned_count + self.approval_count + self.managing_count

    @hybrid_property
    def full_name(self):
        return f"{self.name} / {self.department}"


class IssueTrackerMailing(Base):
    __tablename__ = "issue_tracker_mailing"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    solution_id = Column(Integer, ForeignKey("issue_tracker_solution.id"))
    solution = relationship(
        "IssueTrackerSolution", backref=backref("mailing", uselist=False)
    )
    to = relationship(
        "IssueTrackerUser",
        secondary=default_mailing_to_association_table,
        backref="default_to",
    )
    cc = relationship(
        "IssueTrackerUser",
        secondary=default_mailing_cc_association_table,
        backref="default_cc",
    )


class IssueTrackerSolution(Base):
    __tablename__ = "issue_tracker_solution"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    prod_corp = Column(String(50))
    user_id = Column(String(50), ForeignKey("issue_tracker_user.username"))
    manager = relationship("IssueTrackerUser", backref=backref("manage_solution"))
    issues = relationship("IssueTracker", backref="solution")
    __table_args__ = (
        UniqueConstraint("name", "prod_corp", name="_solution_prod_corp_uc"),
    )


class IssueTrackerHistory(Base):
    __tablename__ = "issue_tracker_history"

    id = Column(Integer, primary_key=True)
    history_type = Column(String(50))
    note = Column(mysql.LONGTEXT)
    created_at = Column(DateTime, default=datetime.now)
    issue_id = Column(Integer, ForeignKey("issue_tracker.id"))
    author_id = Column(String(50), ForeignKey("issue_tracker_user.username"))


class IssueTrackerComment(Base):
    __tablename__ = "issue_tracker_comment"

    id = Column(Integer, primary_key=True)
    comment_type = Column(String(50))
    content = Column(mysql.LONGTEXT, index=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    issue_id = Column(Integer, ForeignKey("issue_tracker.id", ondelete="CASCADE"))
    author_id = Column(
        String(50), ForeignKey("issue_tracker_user.username", ondelete="CASCADE")
    )
    parent_id = Column(Integer, ForeignKey("issue_tracker_comment.id"))
    files = relationship(
        "IssueTrackerCommentFiles",
        backref="issue_tracker_comment",
        passive_deletes=True,
    )
    replies = relationship(
        "IssueTrackerComment",
        backref=backref("parent", remote_side=[id]),
    )


class AttachFileMixin(object):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    status = Column(String(50))
    file_path = Column(String(200))
    file_type = Column(String(100))
    file_size = Column(Integer)
    created_by = Column(String(50))
    created_at = Column(DateTime, default=sql.func.now())
    last_modified_at = Column(DateTime)


class IssueTrackerFiles(AttachFileMixin, Base):
    __tablename__ = "issue_tracker_files"

    issue_id = Column(Integer, ForeignKey("issue_tracker.id"))


class IssueTrackerCommentFiles(AttachFileMixin, Base):
    __tablename__ = "issue_tracker_comment_files"

    comment_id = Column(
        Integer, ForeignKey("issue_tracker_comment.id", ondelete="CASCADE")
    )
