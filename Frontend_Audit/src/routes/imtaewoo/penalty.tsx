import { faEdit, faPaperclip, faTimes } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Alert, Button, Form, List, message, Popconfirm, Popover, Result, Table, Tooltip } from 'antd';
import type { ColumnsType } from 'antd/lib/table';
import axios from 'axios';
import type { Moment } from 'moment';
import moment from 'moment';
import { useSession } from 'next-auth/react';
import { useState } from 'react';
import useSWR from 'swr';

import { ButtonWithFetch } from '@/components/button';
import PenaltyForm from '@/components/PenaltyForm';
import { tableColumnTextFilterConfig } from '@/lib/table';
import { getDeveloper, getProdGroup, getProdGroup_Penalty } from '@/util/Appconfig';
import { string } from 'prop-types';
import { isNull } from 'lodash';

type Data = {
  id: number;
  issue_date: string;
  penalty_date: string;
  heqm_code: string;
  document_type: string;
  reason_code: string;
  division_name: string;
  category_code: string;
  vendor_code: string;
  vendor_name: string;
  part_name: string;
  manager_name: string;
  contents: string;
  status: string;
  created_date: string;
  created_by: string;
  modified_date: string;
  modified_by: string;
  files: Array<Files>;
};

type From = {
  issue_date: Moment;
  penalty_date: Moment;
  heqm_code: string;
  document_type: string;
  reason_code: string;
  division_name: string;
  category_code: string;
  vendor_code: string;
  vendor_name: string;
  part_name: string;
  manager_name: string;
  status: string;
  id: number;
  created_date: string;
  created_by: string;
  modified_date: string;
  modified_by: string;
  files: Array<Files>;
};

type Files = {
  id: number;
  name: string;
  status: string;
  file_path: string;
  file_type: string;
  file_size: number;
  created_by: string;
  created_date: string;
  last_modified_date: string;
};

export default function Penalty() {
  const { data: session } = useSession();
  const { data, error, mutate } = useSWR<Data[]>(`/apis/penalty`);

  const [visible, setVisible] = useState('');
  const [form] = Form.useForm<From>();

  const handleCreate = () => {
    form.resetFields();
    setVisible('create');
  };

  const handleUpdate = (record: Data) => {
    //const values = { ...record, issue_date: moment(record.issue_date, 'YYYY-MM-DD'), penalty_date: moment(record.penalty_date, 'YYYY-MM-DD') };
    const values = { ...record, issue_date: moment(record.issue_date, 'YYYY-MM-DD') };
    form.resetFields();
    form.setFieldsValue(values);
    setVisible('update');
  };

  const handleCreateSubmit = () => {
    form
      .validateFields()
      .then((res) => {

        const values = { ...res, issue_date: res.issue_date.format('YYYY-MM-DD') }; 

        //const values = { ...res, issue_date: res.issue_date.format('YYYY-MM-DD'), 
        //                         penalty_date: res.penalty_date.format('YYYY-MM-DD') };  
        
        //const values = { ...res, issue_date: res.issue_date.format('YYYY-MM-DD'), penalty_date: res.penalty_date.format('YYYY-MM-DD') ?? null}; 
      
        //const values = { ...res, issue_date: res.issue_date.format('YYYY-MM-DD'), 
        //                           penalty_date: res.penalty_date.isValid() === true ? res.penalty_date.format('YYYY-MM-DD') : null };         
                                   
        //console.log('Validate Failed:', res.penalty_date.format('YYYY-MM-DD'));                           
        
        axios
          .post<Data>(`/apis/penalty`, values, {
            withCredentials: true,
          })
          .then((response) => {
            message.success(
              `${response.data.vendor_name} ${response.data.part_name} ${response.data.document_type} registered successfully`,
            );
            setVisible('');
            mutate();
          });
      })
      .catch(() => {
        // console.log('Validate Failed:', info);        
      });
  };

  const handleUpdateSubmit = () => {
    form
      .validateFields()
      .then((res) => {
        const values = { ...res, issue_date: res.issue_date.format('YYYY-MM-DD') };
        //const values = { ...res, issue_date: res.issue_date.format('YYYY-MM-DD'), penalty_date: res.penalty_date.format('YYYY-MM-DD') };

        axios
          .put<Data>(`/apis/penalty/${values.id}`, values, {
            withCredentials: true,
          })
          .then((response) => {
            // console.log(response);
            message.success(
              `${response.data.vendor_name} ${response.data.part_name} ${response.data.document_type} updated successfully`,
            );
            setVisible('');
            mutate();
          });
      })
      .catch(() => {
        // console.log('Validate Failed:', info);
      });
  };

  const handleDelete = (record: Data) => {
    axios
      .delete(`/apis/penalty/${record.id}`, {
        withCredentials: true,
      })
      .then(() => {
        message.success(`${record.vendor_name} ${record.part_name} penalty result has been deleted.`);
        mutate();
      });
  };

  const columns: ColumnsType<Data> = [
    {
      title: '사업부', // 'Division',
      dataIndex: 'category_code',
      key: 'category_code',
      align: 'center',
//      filters: getProdGroup().map((product: string) => ({
      filters: getProdGroup_Penalty().map((product: string) => ({  
        text: product,
        value: product,
      })),
      onFilter: (value: string, record) => record.category_code.includes(value),
    },

    //{
      
    //title: '날짜', //'Date',
    //children: [

    {
      title: '이슈발생일', //'Issue Date',
      dataIndex: 'issue_date',
      key: 'issue_date',
      fixed: 'left',
      align: 'center',
      defaultSortOrder: 'descend',
      sorter: (a, b) => Date.parse(a.issue_date) - Date.parse(b.issue_date),
      ...tableColumnTextFilterConfig<Data>(),
      onFilter: (value: string, record) => {
        return record.issue_date.includes(value);
      },
    },
    /*
    {
      title: 'Penalty Date', // '날짜',
      dataIndex: 'penalty_date',
      key: 'penalty_date',
      fixed: 'left',
      align: 'center',
      defaultSortOrder: 'descend',
      sorter: (a, b) => Date.parse(a.penalty_date) - Date.parse(b.penalty_date),
      ...tableColumnTextFilterConfig<Data>(),
      onFilter: (value: string, record) => {
        return record.penalty_date.includes(value);
      },
    },
    */
    //],
    //},

    //{
    // shyun.park 230610 : Supplier 정보 묶음
    //title: 'Supplier', // '협력회사',
    //  children: [
        {
          title: '협력회사명', // 'Name', // '회사이름',
          dataIndex: 'vendor_name',
          key: 'vendor_name',
          fixed: 'left',
          align: 'center',
          ...tableColumnTextFilterConfig<Data>(),
          onFilter: (value: string, record) => {
            return record.vendor_name.toLowerCase().includes(value.toLowerCase());
          },
        },
        /*
        {
          title: 'Code', // '회사코드',
          dataIndex: 'vendor_code',
          key: 'vendor_code',
          align: 'center',
          ...tableColumnTextFilterConfig<Data>(),
          onFilter: (value: string, record) => {
            return record.vendor_code.toLowerCase().includes(value.toLowerCase());
          },
        },
        */        
    //  ],
    //},    
    {
    // shyun.park 230610 : Part 정보 묶음
    title: '부품', //'Part',
    children: [
        {
          title: '구분', //'CMDT', 
          dataIndex: 'division_name',
          key: 'division_name',
          fixed: 'left',
          align: 'center',
          filters: [            
            { text: '사출', value: '사출' },            
            { text: '판금', value: '판금' },
            { text: '절삭', value: '절삭' },
            { text: '전장', value: '전장' },
            { text: '회로', value: '회로' },  
            { text: '기타', value: '기타' },          
          ],
          onFilter: (value: string, record) => record.division_name.includes(value),
        },
        {
          title: '부품명', //'Part Name',
          dataIndex: 'part_name',
          key: 'part_name',
          align: 'center',
          ...tableColumnTextFilterConfig<Data>(),
          onFilter: (value: string, record) => {
            return record.part_name.toLowerCase().includes(value.toLowerCase());
          },
        },
      ],
    },
    {
    // shyun.park 230610 : 패널티 발행 정보 묶음
    title: '처리 결과', //'Penalty', // '패널티 발행',
    children: [
        {
          title: '발행 유형', //'Penalty Type', // '분류',
          dataIndex: 'document_type',
          key: 'document_type',
          align: 'center',
          filters: [
            { text: '경고장', value: '경고장' }, // { text: 'Warning Letter', value: '경고장' }, 
            // { text: 'Guarantee Letter', value: '개런티 레터' }, // { text: '개런티 레터', value: '개런티 레터' },
            { text: '품질개선요청서', value: '품질개선요청서' }, // { text: 'Quality Improvement Request Form', value: '품질개선요청서' }, 
          ],
          onFilter: (value: string, record) => record.document_type.includes(value),
        },
        {
          title: '발행일', //'Penalty Date'
          dataIndex: 'contents',
          key: 'contents',          
          align: 'center',
          ...tableColumnTextFilterConfig<Data>(),
          onFilter: (value: string, record) => {
            return record.contents.toLowerCase().includes(value.toLowerCase());
          },
        },        
        {
          title: '사유', //'Reason Type', // '구분',
          dataIndex: 'reason_code',
          key: 'reason_code',
          align: 'center',
          filters: [
            { text: '기본 미준수', value: '기본 미준수' }, // { text: 'Basic nonfulfillment', value: '기본 미준수' }, 
            { text: '4M 미신고', value: '4M 미신고' }, // { text: '4M Not Reported', value: '4M 미신고' }, 
            // { text: 'Field Defect', value: '시장 불량' }, // { text: '시장 불량', value: '시장 불량' },
            { text: '품질 이슈', value: '품질 이슈' },
            { text: '정도경영 위반', value: '정도경영 위반' },
            { text: 'CSR/대외법률 위반', value: 'CSR/대외법률 위반' },
            { text: '정보보안 위반', value: '정보보안 위반' },
            { text: '화재 발생', value: '화재 발생' },
          ],
          onFilter: (value: string, record) => record.reason_code.includes(value),
          render: (text, record) => (
            <Tooltip placement="top" title={record.contents}>
              {text}
            </Tooltip>
          ),
        },    
        {
          title: '첨부', //'Attachment', 
          key: 'file',
          // width: 130,
          fixed: 'right',
          align: 'center',
          render: (_, record) => (
            <Popover
              placement="topRight"
              trigger={session && record.files.length !== 0 ? 'click' : ''}
              content={
                <List
                  size="small"
                  className="w-80"
                  dataSource={record.files}
                  renderItem={(file) => (
                    <ButtonWithFetch
                      type="text"
                      file_path={`/apis/penalty/file/${file.id}`}
                      file_name={file.name}
                      file_size={file.file_size}
                    >
                      {file.name}
                    </ButtonWithFetch>
                  )}
                />
              }
            >
              <Button
                type="link"
                icon={<FontAwesomeIcon icon={faPaperclip} />}
                disabled={!(session && record.files.length !== 0)}
              />
            </Popover>
          ),
        },
        {
          title: '담당자', //'Issued Owner',
          dataIndex: 'manager_name',
          key: 'manager_name',
          width: 200,
          align: 'center',
          ...tableColumnTextFilterConfig<Data>(),
          onFilter: (value: string, record) => {
            return record.manager_name.toLowerCase().includes(value.toLowerCase());
          },
        },
        {
          title: '상태', //'Status', // '조치현황',
          dataIndex: 'status',
          key: 'status',          
          align: 'center',
          filters: [
            { text: 'Open', value: 'Open' },
            { text: 'Closed', value: 'Closed' },
          ],
          onFilter: (value: string, record) => record.status.includes(value),
        },
      ],
    },
    /*
    {
      // shyun.park 230610 : 패널티 발행 사유 묶음
      title: 'Issued Reason', // '발행사유',
      children: [
        {
          title: 'Reason Type', // '구분',
          dataIndex: 'reason_code',
          key: 'reason_code',
          align: 'center',
          filters: [
            { text: 'Basic nonfulfillment', value: '기본 미준수' }, // { text: '기본 미준수', value: '기본 미준수' },
            { text: '4M Not Reported', value: '4M 미신고' }, // { text: '4M 미신고', value: '4M 미신고' },
            { text: 'Field Defect', value: '시장 불량' }, // { text: '시장 불량', value: '시장 불량' },
          ],
          onFilter: (value: string, record) => record.reason_code.includes(value),
          render: (text, record) => (
            <Tooltip placement="top" title={record.contents}>
              {text}
            </Tooltip>
          ),
        },    
        {
          title: 'Detail', // '상세정보',
          dataIndex: 'heqm_code',
          key: 'heqm_code',
          align: 'center',
          render: (text: string) => (
            <a
              href="#heqm"
              onClick={() => {
                window.open(`http://heqm.lge.com/#issue_viewer/daily/${text}`);
              }}
              aria-hidden="true"
            >
              {text}
            </a>
          ),
        },
      ],
    },
    */
    /*
    {
      title: 'Status', // '조치현황',
      dataIndex: 'status',
      key: 'status',
      align: 'center',
      filters: [
        { text: 'Open', value: 'Open' },
        { text: 'Closed', value: 'Closed' },
      ],
      onFilter: (value: string, record) => record.status.includes(value),
    },
    */
    {
      title: '수정', //'Edit', 
      key: 'edit',
      width: 50,
      align: 'center', //fixed: 'right',
      render: (_, record) => (
        <Button
          type="link"
          icon={<FontAwesomeIcon icon={faEdit} />}
          disabled={!(session && session.user.username === record.created_by)}
          onClick={() => handleUpdate(record)}
        />
      ),
    },
    {
      title: '삭제', //'Del',
      key: 'delete',
      width: 50,
      align: 'center', //fixed: 'right',
      render: (_, record) => (
        <Popconfirm
          title="정말로 삭제하시겠습니까?"
          placement="topRight"
          onConfirm={() => handleDelete(record)}
          okText="Yes"
          cancelText="No"
          disabled={!(session && session.user.username === record.created_by)}
        >
          <Button
            type="link"
            icon={<FontAwesomeIcon icon={faTimes} />}
            disabled={!(session && session.user.username === record.created_by)}
          />
        </Popconfirm>
      ),
    },
  ];

  if (error)
    return <Result status="error" title="Error" subTitle="There is a problem. Please contact system administrator." />;

  return (
    <>
      <Alert
        className="mb-5"
        message={`이 기능은 현재 개발 중으로 잦은 오류가 발생 될 수 있습니다. 오류 발생 시 관리자 (${getDeveloper()})에게 알려주세요.`}
        type="warning"
        closable
      />
      <Table
        rowKey="id"
        columns={columns}
        dataSource={data}
        scroll={{ x: 1000 }}
        size="small"
        loading={!data}
        bordered
        footer={() => (
          <div style={{ textAlign: 'right' }}>
            <Button type="primary" onClick={handleCreate} disabled={!session}>
              New
            </Button>
          </div>
        )}
      />
      <PenaltyForm
        form={form}
        title="패널티 문서 신규 등록"
        visible={visible === 'create'}
        okText="Create"
        onOk={handleCreateSubmit}
        onCancel={() => setVisible('')}
      />
      <PenaltyForm
        form={form}
        title="패널티 문서 업데이트"
        visible={visible === 'update'}
        okText="Update"
        onOk={handleUpdateSubmit}
        onCancel={() => setVisible('')}
      />
    </>
  );
}