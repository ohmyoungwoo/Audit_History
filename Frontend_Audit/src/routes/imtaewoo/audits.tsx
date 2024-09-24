import { faCloudUploadAlt, faEdit, faPaperclip, faTimes } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Alert, Button, message, Modal, Result, Table, Typography, Upload } from 'antd';
import type { ColumnsType } from 'antd/lib/table';
import type { AxiosError } from 'axios';
import axios from 'axios';
import moment from 'moment';
import { useSession } from 'next-auth/react';
import { useRef, useState } from 'react';
import useSWR from 'swr';

import { ButtonWithFetch } from '@/components/button';
import CounterMeasureModal from '@/components/countermeasureModal';
import { safeDivide } from '@/lib/common';
import { tableColumnTextFilterConfig } from '@/lib/table';
import { getCompanyAdmin } from '@/util/Appconfig';

const { Link } = Typography;

type RecordProps = {
  id: number;
  vendor_name: string;
  part_name: string;
};

type Data = {
  id: number;
  start_date: string;
  org_name: string;
  vendor_name: string;
  vendor_code: string;
  part_name: string;
  audit_type: string;
  grade: string;
  division_name: string;
  manager_name: string;
  common_score: number;
  common_detail: Array<Score>;
  expertise_score: number;
  expertise_detail: Array<Score>;
  total_score: number;
  countermeasure: Array<Point>;
  file_path: string;
  file_size: number;
  orig_file_name: string;
  created_by: string;
/*
  eco: number;
  total_audit: number;
  prr: number;
  no_work: number;
  total_quality: number;
  plus: number;
  minus: number;
  total_sqd: number;  
  total_grade: string; 
*/  
};

type Score = {
  item: string;
  score: number;
};

type Point = {
  item: string;
  points: string;
  measures: string;
  completion_date: string;
  review_result: string;
  status: string;
  importance: string;
};

type Error = {
  detail: string;
};

export default function Audits() {
  const { data: session } = useSession();
  const { data, error, mutate } = useSWR<Data[]>(`/apis/audit`);
  const [isUploading, setIsUploading] = useState(false);
  const [isScoreVisible, setIsScoreVisible] = useState(false);
  const [isPointsVisible, setIsPointsVisible] = useState(false);

  const editInput = useRef<HTMLInputElement>();
  const [editId, setEditId] = useState<number>(-1);

  const [score, setScore] = useState<Score[]>();
  const [points, setPoints] = useState<Point[]>();

  const totalCount = useRef(0);
  const closeCount = useRef(0);

  const handleDelete = (record: RecordProps) => {
    axios
      .delete(`/apis/audit/${record.id}`, {
        withCredentials: true,
      })
      .then(() => {
        message.success(`${record.vendor_name} ${record.part_name} audit result has been deleted.`);
        mutate();
      });
  };

  const handleUpdate = (e: { target: HTMLInputElement }) => {
    const hide = message.loading('Update in progress..', 0);
    const formData = new FormData();
    formData.append('file', e.target.files[0]);

    axios
      .put(`/apis/audit/${editId}`, formData, {
        withCredentials: true,
      })
      .then((res: { data: Data }) => {
        hide();
        message.success(
          `${res.data.vendor_name} ${res.data.part_name} ${res.data.audit_type} result updated successfully`,
        );
        mutate();
      })
      .catch((err: AxiosError<Error>) => {
        message.error(err.response.data.detail);
      })
      .finally(() => {
        hide();
      });
  };

  const handleClickScore = (record: Array<Score>) => {
    setScore(record);
    setIsScoreVisible(true);
  };

  const handleClickStatus = (record: Array<Point>) => {
    setPoints(record);
    setIsPointsVisible(true);
  };

  const uploadFilesProps = {
    accept: '.xlsx, .xls',
    showUploadList: false,
    beforeUpload: (file: File) => {
      if (session) {
        const formData = new FormData();
        formData.append('file', file);
        setIsUploading(true);
        axios
          .post<Data>(`/apis/audit`, formData, {
            withCredentials: true,
          })
          .then((response) => {
            message.success(
              `${response.data.vendor_name} ${response.data.part_name} ${response.data.audit_type} result uploaded successfully`,
            );
            mutate();
          })
          .catch((err: AxiosError<Error>) => {
            message.error(err.response.data.detail);
          })
          .finally(() => {
            setIsUploading(false);
          });
      }
      return false;
    },
  };

  const columnsDetail: ColumnsType<Score> = [
    {
      title: 'Item',
      dataIndex: 'item',
      key: 'item',
      align: 'center',
      width: 300,
    },
    {
      title: 'Score',
      dataIndex: 'score',
      key: 'score',
      align: 'center',
      render: (value) => Math.round(value * 10) / 10,
    },
  ];

  const columns: ColumnsType<Data> = [
    
    {
      // shyun.park 230609 : Audit Information 묶음
      title: '품질심사 정보', //'Audit Information'
      children: [
        {
          title: '법인', // 'Site',
          dataIndex: 'org_name',
          key: 'org_name',
          align: 'center',
          sorter: (a, b) => Date.parse(a.start_date) - Date.parse(b.start_date),
          filters: [
            // shyun.park 230608
            { text: 'KR', value: 'KR' },
            { text: 'TR', value: 'TR' },
            { text: 'TA', value: 'TA' },
            { text: 'PN', value: 'PN' },
            { text: 'TH', value: 'TH' },
            { text: 'IN', value: 'IN' },
            { text: 'IL', value: 'IL' },
            { text: 'VH', value: 'VH' },
            { text: 'RA', value: 'RA' },
            { text: 'SR', value: 'SR' },
            { text: 'EG', value: 'EG' },
            { text: 'WR', value: 'WR' },
            { text: 'MM', value: 'MM' },
            { text: 'SP', value: 'SP' },
            { text: 'TN', value: 'TN' },
          ],
          onFilter: (value: string, record) => record.org_name.includes(value),
        },
        {
          title: '심사일', // 'Date',
          dataIndex: 'start_date',
          key: 'start_date',
          // width: 120,
          align: 'center',
          defaultSortOrder: 'descend',
          ...tableColumnTextFilterConfig<Data>(),
          sorter: (a, b) => Date.parse(a.start_date) - Date.parse(b.start_date),
          onFilter: (value, record) => {
            return record.start_date.includes(value.toString());
          },
        },
        /*
        {
          title: '타입', // 'Type',
          dataIndex: 'audit_type',
          key: 'audit_type',
          // width: 80,
          align: 'center',
          filters: [
            { text: '품질체제', value: '품질체제' }, // shyun.park 230623 { text: '정기', value: '정기' }, 
            { text: '친환경', value: '친환경' }, // shyun.park 230621 { text: '신규', value: '신규' },
          ],
          onFilter: (value, record) => {
            return record.audit_type.includes(value.toString());
          },
        },
        {
          title: '심사자 소속', // 'Division',
          dataIndex: 'category_code',
          key: 'category_code',
          align: 'center',
          filters: [
            { text: '리빙솔루션', value: '리빙솔루션' },
            { text: '에어솔루션', value: '에어솔루션' },
            { text: '키친솔루션', value: '키친솔루션' },
            { text: '부품솔루션', value: '부품솔루션' },
          ],
          onFilter: (value: string, record) => record.category_code.includes(value),
        },
        */
        {
          title: '심사자', // 'Auditor',
          dataIndex: 'manager_name',
          key: 'manager_name',
          ellipsis: true,
          align: 'center',
        },
      ],
    },
    {
      // shyun.park 230609 : Supplier 정보 묶음
      title: '협력회사', // 'Supplier',
      children: [
        {
          title: '회사이름', // 'Name',
          dataIndex: 'vendor_name',
          key: 'vendor_name',
          align: 'center',
          ellipsis: true,
          ...tableColumnTextFilterConfig<Data>(),
          onFilter: (value, record) => {
            return record.vendor_name.toLowerCase().includes(value.toString().toLowerCase());
          },
        },
        {
          title: '회사코드', // 'Code',
          dataIndex: 'vendor_code',
          key: 'vendor_code',
          align: 'center',
          ellipsis: true,
          ...tableColumnTextFilterConfig<Data>(),
          onFilter: (value, record) => {
            return record.vendor_code.toLowerCase().includes(value.toString().toLowerCase());
          },
        },
      ],
    },
    {
      // shyun.park 230609 : Part 정보 묶음
      title: '부품', // 'Part',
      children: [
        {
          title: '구분', //'부품구분', // 'CMDT',
          dataIndex: 'division_name',
          key: 'division_name',
          align: 'center',
          filters: [
            { text: '사출', value: '사출' },
            { text: '판금', value: '판금' },
            { text: '절삭', value: '절삭' },
            { text: '전장', value: '전장' },
            { text: '회로', value: '회로' },
          ],
          onFilter: (value: string, record) => record.division_name.includes(value),
        },
        {
          title: '부품명', // 'Part Name',
          dataIndex: 'part_name',
          key: 'part_name',
          align: 'center',
          ellipsis: true,
          ...tableColumnTextFilterConfig<Data>(),
          onFilter: (value, record) => {
            return record.part_name.toLowerCase().includes(value.toString().toLowerCase());
          },
        },
      ],
    },    
    /* shyun.park 230608
    {
      title: 'Grade',
      dataIndex: 'grade',
      key: 'grade',
      align: 'center',
      filters: [
        { text: 'S', value: 'S' },
        { text: 'A', value: 'A' },
        { text: 'B', value: 'B' },
        { text: 'C', value: 'C' },
        { text: 'D', value: 'D' },
        { text: 'E', value: 'E' }, 
      ],
      onFilter: (value: string, record) => record.grade.includes(value),
    },
    */
    {
      title: '품질체제 평가결과',//'품질체제(150)', // 'Audit Result',
      children: [
        {
          title: '기본품질(40)', // 'Basic Quality', //'Common parts', shyun.park 230608 
          dataIndex: 'common_score',
          key: 'common_score',
          ellipsis: true,
          align: 'center',
          sorter: (a, b) => a.common_score - b.common_score,
          render: (value, record) => (
            <Link
              onClick={() => {
                handleClickScore(record.common_detail);
              }}
            >
              {Math.round(value * 10) / 10}
            </Link>
          ),
        },
        {
          title: '공정품질(110)', // 'Process Quality', // 'Specialized parts', shyun.park 230608
          dataIndex: 'expertise_score',
          key: 'expertise_score',
          ellipsis: true,
          align: 'center',
          sorter: (a, b) => a.expertise_score - b.expertise_score,
          render: (value, record) => (
            <Link
              onClick={() => {
                handleClickScore(record.expertise_detail);
              }}
            >
              {Math.round(value * 10) / 10}
            </Link>
          ),
        },
        {
          title: '총점(150)', // 'Total Score',
          dataIndex: 'total_score',
          key: 'total_score',
          ellipsis: true,
          align: 'center',
          sorter: (a, b) => a.total_score - b.total_score,
          render: (text) => Math.round(text * 10) / 10,
        },
        {
          // shyun.park 230609 : major만 실적 관리하는 것에서, comment 제외 실적 관리하는 것으로 변경
          title: '이슈 F/Up', //'신호등', // 'Signal',
          key: 'signal',
          //width: 70,
          align: 'center',
          filters: [
            { text: 'Green', value: true },
            { text: 'Red', value: false },
          ],
          onFilter: (value, record) =>
            (record.countermeasure.filter(
              (e) => e.status.toLowerCase() === 'open' && e.importance.toLowerCase() !== 'comment',
            ).length === 0 || moment(record.start_date, 'YYYY-MM-DD') >= moment().subtract(1, 'months')) === value,
          render: (_, record: Data) => (
            <div
              className={`mx-auto h-3 w-3 rounded-full ${
                record.countermeasure.filter(
                  (e) => e.status.toLowerCase() === 'open' && e.importance.toLowerCase() !== 'comment',
                ).length === 0 || moment(record.start_date, 'YYYY-MM-DD') >= moment().subtract(1, 'months')
                  ? 'bg-green-500'
                  : 'bg-red-500'
              }`}
            />
          ),
        },
        {
          title: '진척율', // 'Rate',
          dataIndex: 'countermeasure',
          key: 'rate',
          //width: 80,
          align: 'center',
          render: (value: Array<Point>) => {
            closeCount.current = value.filter(
              (e) => e.status.toLowerCase() === 'closed' && e.importance.toLowerCase() !== 'comment',
            ).length;
            totalCount.current = value.filter((e) => e.importance.toLowerCase() !== 'comment').length;
            return totalCount.current === 0
              ? '100%'
              : `${Math.round(safeDivide(closeCount.current, totalCount.current) * 1000) / 10}%`;
          },
        },
        {
          // shyun.park 230609 : major만 실적 관리하는 것에서, comment 제외 실적 관리하는 것으로 변경
          // title: 'Status',
          title: '진행상세', // 'Detail',
          dataIndex: 'countermeasure',
          key: 'countermeasure',
          //width: 80,
          // ellipsis: true,
          align: 'center',
          filters: [
            { text: '완료', value: true }, //{ text: 'Complete', value: true },
            { text: '진행중', value: false }, //{ text: 'Complete', value: true },
          ],
          onFilter: (value, record) =>
            (record.countermeasure.filter(
              (e) => e.status.toLowerCase() === 'open' && e.importance.toLowerCase() !== 'comment',
            ).length ===
              0) ===
            value,
          render: (value: Array<Point>) => (
            <a
              href="#countermeasure"
              style={{ color: '#A50034' }}
              onClick={() => {
                handleClickStatus(value);
              }}
              aria-hidden="true"
            >
              {value.filter((e) => e.status.toLowerCase() === 'open' && e.importance.toLowerCase() !== 'comment').length === 0
               ? '완료' //'Complete'
               : '진행중'  // 'Ongoing'
              }
            </a>
          ),
        },
      ]
    },
        {
          title: '내려받기', // 'Download',
          key: 'file',
          // width: 120,
          align: 'center',
          render: (_, record) => (
            <ButtonWithFetch
              type="default"
              size="small"
              file_name={`${record.orig_file_name}`}
              file_path={`/apis/audit/file/${record.id}`}
              file_size={record.file_size}
            >
              <FontAwesomeIcon icon={faPaperclip} />
            </ButtonWithFetch>
          ),
        },
        {
          title: '수정', //  'Edit',
          key: 'edit',
          width: 80,
          align: 'center',
          render: (_, record) => (
            <Button
              type="link"
              icon={<FontAwesomeIcon icon={faEdit} />}
              disabled={!(session && session.user.username === record.created_by)}
              onClick={() => {
                setEditId(record.id);
                editInput.current.click();
              }}
            />
          ),
        },    
    /*
    {
      title: '친환경(50)', // 230623 shyun.park
      children: [
        {
          title: '점수', 
          dataIndex: 'eco_score',
          key: 'eco_score',
          ellipsis: true,
          align: 'center',
          
          //sorter: (a, b) => a.common_score - b.common_score,
          //render: (value, record) => (
          //  <Link
          //    onClick={() => {
          //      handleClickScore(record.common_detail);
          //    }}
          //  >
          //    {Math.round(value * 10) / 10}
          //  </Link>
          //),
        },        
        {
          title: '내려받기', // 'Download',
          key: 'file_eco',
          // width: 120,
          align: 'center',
          //render: (_, record) => (
          //  <ButtonWithFetch
          //    type="default"
          //    size="small"
          //    file_name={`${record.orig_file_name}`}
          //    file_path={`/apis/audit/file/${record.id}`}
          //    file_size={record.file_size}
          //  >
          //    <FontAwesomeIcon icon={faPaperclip} />
          //  </ButtonWithFetch>
          //),
        },
        {
          title: '수정', //  'Edit',
          key: 'edit_eco',
          width: 80,
          align: 'center',
          //render: (_, record) => (
          //  <Button
          //    type="link"
          //    icon={<FontAwesomeIcon icon={faEdit} />}
          //    disabled={!(session && session.user.username === record.created_by)}
          //    onClick={() => {
          //      setEditId(record.id);
          //      editInput.current.click();
          //    }}
          //  />
          //),
        },
      ],
    },
    */
    {
      title: '결과 삭제', // 'Del',
      key: 'delete',
      width: 100,
      fixed: 'right',
      align: 'center',
      render: (_, record) => (
        <Button
          type="link"
          icon={<FontAwesomeIcon icon={faTimes} />}
          disabled={!(session && session.user.username === record.created_by)}
          onClick={() => handleDelete(record)}
        />
      ),
    },
  ];

  if (error)
    return <Result status="error" title="Error" subTitle="There is a problem. Please contact system administrator." />;

  return (
    <>
      <Alert
        className="mb-5"
        message={`이 기능은 현재 개발 중으로 잦은 오류가 발생 될 수 있습니다. 오류 발생 시 관리자 ${getCompanyAdmin()}에게 알려주세요.`}
        type="warning"
        closable
      />
      <Table
        rowKey="id"
        columns={columns}
        dataSource={data}
        size="small"
        loading={!data}
        bordered
        footer={() => (
          <div style={{ textAlign: 'right' }}>
            <Upload {...uploadFilesProps}>
              <Button
                type="primary"
                icon={<FontAwesomeIcon icon={faCloudUploadAlt} />}
                loading={isUploading}
                disabled={!session}>
                 파일 올리기
              </Button>
            </Upload>
          </div>
        )}
      />
      <Modal
        title="상세현황" // "Score Detail"
        transitionName=""
        maskTransitionName=""
        visible={isScoreVisible}
        width={450}
        onCancel={() => setIsScoreVisible(false)}
        footer={null}
      >
        <Table
          rowKey="order"
          columns={columnsDetail}
          dataSource={score}
          size="small"
          loading={!score}
          pagination={false}
          bordered
          summary={(pageData) => {
            let total = 0;
            pageData.forEach((value) => {
              total += parseFloat(value.score.toString());
            });

            return (
              <Table.Summary.Row>
                <Table.Summary.Cell index={1} align="center">
                  Total
                </Table.Summary.Cell>
                <Table.Summary.Cell index={2} align="center">
                  {Math.round(total * 10) / 10}
                </Table.Summary.Cell>
              </Table.Summary.Row>
            );
          }}
        />
      </Modal>
      <CounterMeasureModal data={points} isVisible={isPointsVisible} setIsVisible={setIsPointsVisible} />
      <input
        ref={editInput}
        onChange={handleUpdate}
        type="file"
        style={{ display: 'none' }}
        accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        multiple={false}
      />
    </>
  );
}
