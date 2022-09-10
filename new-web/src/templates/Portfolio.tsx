import { useState, useEffect } from 'react';

import { useRouter } from 'next/router';
import { InfinitySpin } from 'react-loader-spinner';
import initSqlJs from 'sql.js';

import { Meta } from '../layout/Meta';
import { AppConfig } from '../utils/AppConfig';
import { Footer } from './Footer';
import { Header } from './Header';

/**
 * Renders a single value of the array returned by db.exec(...) as a table
 * @param {import("sql.js").QueryExecResult} props
 */
function ResultsTable({ columns, values }) {
  return (
    <table>
      <thead>
        <tr>
          {columns.map((columnName, i) => (
            <td key={i}>{columnName}</td>
          ))}
        </tr>
      </thead>

      <tbody>
        {
          // values is an array of arrays representing the results of the query
          values.map((row, i) => (
            <tr key={i}>
              {row.map((value, i) => (
                <td key={i}>{value}</td>
              ))}
            </tr>
          ))
        }
      </tbody>
    </table>
  );
}

const Portfolio = () => {
  const [db, setDb] = useState<any>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<any>(null);
  const [results, setResults] = useState([]);
  const router = useRouter();

  function exec(sqlDB: any, sql: string) {
    try {
      // The sql is executed synchronously on the UI thread.
      // You may want to use a web worker here instead
      setResults(sqlDB.exec(sql)); // an array of objects is returned
      setError(null);
    } catch (err) {
      // exec throws an error when the SQL statement is invalid
      setError(err);
      setResults([]);
    }
  }

  useEffect(() => {
    async function fetchData() {
      if (!router.isReady) return;

      const traderName = router.query.t as string;
      const portfolioName = router.query.p as string;

      const sqlPromise = initSqlJs({
        // Fetch sql.js wasm file from CDN
        // This way, we don't need to deal with webpack
        locateFile: (file: any) =>
          `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/${file}`,
      });
      const dbURL = `https://www.i365.tech/invest-alchemy/data/portfolio/${traderName}/${portfolioName}/${portfolioName}.db`;
      const dataPromise = fetch(dbURL).then((res) => res.arrayBuffer());
      const [SQL, buf] = await Promise.all([sqlPromise, dataPromise]);
      const sqlDB = new SQL.Database(new Uint8Array(buf));
      setDb(sqlDB);
      setLoading(false);
      exec(
        sqlDB,
        'select trade_date as td, net_value as nv from portfolio_net_value_ledger order by trade_date desc limit 10;'
      );
    }
    fetchData();
  }, [router]);

  return (
    <div className="antialiased text-gray-600">
      <Meta title={AppConfig.title} description={AppConfig.description} />
      <Header />
      <div className="flex items-center justify-center h-screen">
        {loading && <InfinitySpin width="200" color="#EAB308" />}
        <pre className="error">{(error || '').toString()}</pre>
        <pre>
          {
            // results contains one object per select statement in the query
            results.map(({ columns, values }, i) => (
              <ResultsTable key={i} columns={columns} values={values} />
            ))
          }
        </pre>
      </div>
      <Footer />
    </div>
  );
};

export { Portfolio };
