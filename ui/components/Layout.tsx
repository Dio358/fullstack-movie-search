import React, { ReactNode } from "react";
import Head from "next/head";

type Props = {
  children?: ReactNode;
  title?: string;
};

const Layout = ({ children, title = "This is the default title" }: Props) => (
  <div
    style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg,rgb(0, 0, 0),rgb(42,42,42))",
    }}
  >
    <div
      style={{
        content: '""',
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "rgba(255, 255, 255, 0.1)", 
        zIndex: 0,
      }}
    />
    <Head>
      <title>{title}</title>
      <meta charSet="utf-8" />
      <meta name="viewport" content="initial-scale=1.0, width=device-width" />
    </Head>

    <div style={{ position: "relative", zIndex: 1 }}>{children}</div>
  </div>
);

export default Layout;
