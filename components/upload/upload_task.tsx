import { Upload, message, Row, Col } from "antd";
import { InboxOutlined } from "@ant-design/icons";
import { getBaseUrl } from "../common/http";

const { Dragger } = Upload;

interface UploadTaskProps {
  uploadComplete: (index: number) => void;
}

export function UploadTask(props: UploadTaskProps) {
  const draggerProps = {
    name: "file",
    multiple: false,
    accept: ".jpg",
    action: getBaseUrl() + "/upload-image",
    onChange(info) {
      if (info.file.status === "done") {
        message.success(`${info.file.name} file uploaded successfully`);
        props.uploadComplete(info.file.response.index);
      } else if (info.file.status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      }
    },
    onDrop(e) {
      console.log("Dropped files", e.dataTransfer.files);
    },
  };

  return (
    <Col span={24}>
      <Dragger {...draggerProps}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-hint">Upload images</p>
      </Dragger>
    </Col>
  );
}
