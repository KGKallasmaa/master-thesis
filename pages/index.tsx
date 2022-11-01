import Upload from "../components/upload/upload";
import Head from "next/head";

export default function UploadPage() {
  return (
    <>
      <Head>
        <title>Explaining machine learning</title>
        <meta name="description" content="Upload your image to explain it" />
      </Head>
      <Upload />
    </>
  );
}
