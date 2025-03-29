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
      background: "linear-gradient(135deg,rgba(75, 177, 68, 0.42),rgba(61, 125, 234, 0.36))",
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

    {/* content goes above the overlay */}
    <div style={{ position: "relative", zIndex: 1 }}>{children}</div>
  </div>
);

export default Layout;
