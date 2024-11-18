import type { Metadata } from "next";
// import { Inter } from "next/font/google";
import "./globals.css";
import { Container, Row, Col, Button } from 'react-bootstrap';
// import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import TopBar from '@/comp/TopBar';
import wdyr from '@welldone-software/why-did-you-render';
// const inter = Inter({ subsets: ["latin"] });

wdyr(React, { logOnDifferentValues: true });
export const metadata: Metadata = {
  title: "InnoWeaver",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css" rel="stylesheet" />
      </head>
      {/* <body className={inter.className}>{children}</body> */}
      <body>
        <TopBar />
        <div>
          {children}
        </div>
      </body>
    </html>
  );
}
