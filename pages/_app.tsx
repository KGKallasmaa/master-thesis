import "../styles/globals.css";
import "antd/dist/antd.css";
import Footer from "../components/common/footer";
import { Toaster } from "react-hot-toast";

function MyApp({ Component, pageProps }) {
  return (
    <>
      <div>
        <Toaster />
      </div>
      <Component {...pageProps} />
      <Footer />
    </>
  );
}

export default MyApp;
