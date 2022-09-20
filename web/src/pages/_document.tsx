import Document, { Html, Head, Main, NextScript } from 'next/document';

import { AppConfig } from '../utils/AppConfig';

// Need to create a custom _document because i18n support is not compatible with `next export`.
class MyDocument extends Document {
  render() {
    return (
      <Html lang={AppConfig.locale}>
        <Head>
          <meta name="application-name" content={AppConfig.title} />
          <meta name="apple-mobile-web-app-capable" content="yes" />
          <meta
            name="apple-mobile-web-app-status-bar-style"
            content="default"
          />
          <meta name="apple-mobile-web-app-title" content={AppConfig.title} />
          <meta name="description" content={AppConfig.description} />
          <meta name="format-detection" content="telephone=no" />
          <meta name="mobile-web-app-capable" content="yes" />
          <meta name="msapplication-TileColor" content="#2B5797" />
          <meta name="msapplication-tap-highlight" content="no" />
          <meta name="theme-color" content="#000000" />

          <link rel="apple-touch-icon" href="/apple-touch-icon.png" />

          <link
            rel="icon"
            type="image/png"
            sizes="32x32"
            href="favicon-32x32.png"
          />
          <link
            rel="icon"
            type="image/png"
            sizes="16x16"
            href="favicon-16x16.png"
          />
          <link rel="manifest" href="/manifest.json" />
          <link rel="shortcut icon" href="/favicon.ico" />
          <link
            rel="stylesheet"
            href="https://fonts.googleapis.com/css?family=Roboto:300,400,500"
          />

          <meta name="twitter:card" content={AppConfig.description} />
          <meta name="twitter:url" content={AppConfig.canonical} />
          <meta name="twitter:title" content={AppConfig.title} />
          <meta name="twitter:description" content={AppConfig.description} />
          <meta
            name="twitter:image"
            content="https://money.bmpi.dev/android-chrome-192x192.png"
          />
          <meta name="twitter:creator" content="@madawei2699" />
          <meta property="og:type" content="website" />
          <meta property="og:title" content={AppConfig.title} />
          <meta property="og:description" content={AppConfig.description} />
          <meta property="og:site_name" content={AppConfig.title} />
          <meta property="og:url" content={AppConfig.canonical} />
          <meta
            property="og:image"
            content="https://money.bmpi.dev/apple-touch-icon.png"
          />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}

export default MyDocument;
