import "../styles/globals.css";
import "antd/dist/antd.css";
import Footer from "../components/common/footer";

function MyApp({ Component, pageProps }) {
  return <>
    <Component {...pageProps} />
    <Footer/>
    </>;
}

export default MyApp;
