import { useState, useEffect } from 'react';

import ReactECharts from 'echarts-for-react';
import { useRouter } from 'next/router';
import { InfinitySpin } from 'react-loader-spinner';
import initSqlJs from 'sql.js';

import { Meta } from '../layout/Meta';
import { AppConfig } from '../utils/AppConfig';
import { getPortfolioByName } from '../utils/PortfolioConfig';
import { Footer } from './Footer';
import { Header } from './Header';

const Portfolio = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<any>(null);
  const [options, setOptions] = useState({});
  const [portfolio, setPortfolio] = useState<any>();
  const router = useRouter();

  function exec(sqlDB: any, sql: string) {
    const results = sqlDB.exec(sql);
    return [].concat(...results[0].values);
  }

  useEffect(() => {
    async function fetchData() {
      try {
        if (!router.isReady) return;

        const traderName = router.query.t as string;
        const portfolioName = router.query.p as string;

        setPortfolio(getPortfolioByName(portfolioName));

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
        // exec(
        //   sqlDB,
        //   'select portfolio_nv, zz500_nv, hs300_nv, cyb_nv, hsi_nv, spx_nv, ixic_nv, gdaxi_nv, n225_nv, ks11_nv, as51_nv, sensex_nv, base15_nv from portfolio_index_compare_ledger order by trade_date;'
        // );
        const optionsData = {
          grid: {
            top: 100,
            right: 8,
            bottom: 24,
            left: 36,
          },
          legend: {
            data: [
              '组合净值',
              '中证500',
              '沪深300',
              '创业板',
              '恒生指数',
              '标普500',
              '纳斯达克',
              '德国DAX',
              '日经225',
              '韩国综合',
              '澳大利亚标普200',
              '印度孟买',
              '15%基准',
            ],
            bottom: 'auto',
          },
          xAxis: {
            type: 'category',
            data: exec(
              sqlDB,
              'select trade_date from portfolio_index_compare_ledger order by trade_date asc'
            ),
          },
          yAxis: {
            type: 'value',
          },
          series: [
            {
              name: '组合净值',
              data: exec(
                sqlDB,
                'select portfolio_nv from portfolio_index_compare_ledger order by trade_date asc'
              ),
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 2,
              },
            },
            {
              name: '中证500',
              data: exec(
                sqlDB,
                'select zz500_nv from portfolio_index_compare_ledger order by trade_date asc'
              ),
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 1,
              },
              showSymbol: false,
            },
            {
              name: '沪深300',
              data: exec(
                sqlDB,
                'select hs300_nv from portfolio_index_compare_ledger order by trade_date asc'
              ),
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 1,
              },
              showSymbol: false,
            },
            {
              name: '创业板',
              data: exec(
                sqlDB,
                'select cyb_nv from portfolio_index_compare_ledger order by trade_date asc'
              ),
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 1,
              },
              showSymbol: false,
            },
            {
              name: '恒生指数',
              data: exec(
                sqlDB,
                'select hsi_nv from portfolio_index_compare_ledger order by trade_date asc'
              ),
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 1,
              },
              showSymbol: false,
            },
            {
              name: '标普500',
              data: exec(
                sqlDB,
                'select spx_nv from portfolio_index_compare_ledger order by trade_date asc'
              ),
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 1,
              },
              showSymbol: false,
            },
            {
              name: '纳斯达克',
              data: exec(
                sqlDB,
                'select ixic_nv from portfolio_index_compare_ledger order by trade_date asc'
              ),
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 1,
              },
              showSymbol: false,
            },
            {
              name: '德国DAX',
              data: exec(
                sqlDB,
                'select gdaxi_nv from portfolio_index_compare_ledger order by trade_date asc'
              ),
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 1,
              },
              showSymbol: false,
            },
            {
              name: '日经225',
              data: exec(
                sqlDB,
                'select n225_nv from portfolio_index_compare_ledger order by trade_date asc'
              ),
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 1,
              },
              showSymbol: false,
            },
            {
              name: '韩国综合',
              data: exec(
                sqlDB,
                'select ks11_nv from portfolio_index_compare_ledger order by trade_date asc'
              ),
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 1,
              },
              showSymbol: false,
            },
            {
              name: '澳大利亚标普200',
              data: exec(
                sqlDB,
                'select as51_nv from portfolio_index_compare_ledger order by trade_date asc'
              ),
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 1,
              },
              showSymbol: false,
            },
            {
              name: '印度孟买',
              data: exec(
                sqlDB,
                'select sensex_nv from portfolio_index_compare_ledger order by trade_date asc'
              ),
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 1,
              },
              showSymbol: false,
            },
            {
              name: '15%基准',
              data: exec(
                sqlDB,
                'select base15_nv from portfolio_index_compare_ledger order by trade_date asc'
              ),
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 0.5,
                type: 'dotted',
              },
              showSymbol: false,
            },
          ],
          tooltip: {
            trigger: 'axis',
            order: 'valueDesc',
          },
        };
        setOptions(optionsData);
      } catch (err) {
        setError(err);
      }
      setLoading(false);
    }
    fetchData();
  }, [router]);

  return (
    <div className="antialiased text-gray-600">
      <Meta title={AppConfig.title} description={AppConfig.description} />
      <Header />
      <div className="flex flex-col items-center justify-center mb-20">
        {loading && <InfinitySpin width="200" color="#EAB308" />}
        <pre className="error">{(error || '').toString()}</pre>
        {portfolio && (
          <div className="m-6 text-center">
            <div className="text-2xl font-bold text-yellow-500">
              {portfolio.title}
            </div>
            <div className="text-sm text-gray-500">{portfolio.description}</div>
          </div>
        )}

        {/* <div className="grid grid-cols-10 gap-8 mb-6 border-2 py-3">
          <div>01</div>
          <div>01</div>
          <div>01</div>
          <div>01</div>
          <div>01</div>
          <div>01</div>
          <div>01</div>
          <div>01</div>
          <div>01</div>
          <div>09</div>
        </div> */}

        <div className="sm:w-9/12 w-11/12">
          {!loading && (
            <ReactECharts option={options} style={{ height: 800 }} />
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export { Portfolio };
