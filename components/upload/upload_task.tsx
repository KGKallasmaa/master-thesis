import {Upload, message, Row} from 'antd';
import {InboxOutlined} from '@ant-design/icons';

const {Dragger} = Upload;

interface UploadTaskProps {
    label: string,
}

export function UploadTask(props: UploadTaskProps) {
    const {label} = props

    const draggerProps = {
        name: 'file',
        multiple: true,
        action: 'https://www.mocky.io/v2/5cc8019d300000980a055e76',
        onChange(info) {
            const {status} = info.file;
            if (status !== 'uploading') {
                console.log(info.file, info.fileList);
            }
            if (status === 'done') {
                message.success(`${info.file.name} file uploaded successfully.`);
            } else if (status === 'error') {
                message.error(`${info.file.name} file upload failed.`);
            }
        },
        onDrop(e) {
            console.log('Dropped files', e.dataTransfer.files);
        }
    }

    return (
        <>
            <h3>Upload images</h3>
            <p>Upload images associated with <b>{label}</b></p>
            <br/>
            <Row>
                <Dragger {...draggerProps} style={{width: 500}}>
                    <p className="ant-upload-drag-icon">
                        <InboxOutlined/>
                    </p>
                    <p className="ant-upload-hint">
                        Upload images
                    </p>
                </Dragger>
            </Row>
        </>
    )
}