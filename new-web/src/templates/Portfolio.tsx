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
  const router = useRouter();

  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<any>(null);
  const [options, setOptions] = useState({});
  const [portfolio, setPortfolio] = useState<any>();
  const [netValue, setNetValue] = useState<string>();
  const [latestTradeDate, setLatestTradeDate] = useState<string>();
  const [firstFundingDate, setFirstFundingDate] = useState<string>();
  const [performance, setPerformance] = useState<string[]>();
  const [currentTab, setCurrentTab] = useState<string>('transaction');
  const [transactions, setTransactions] = useState<string[]>();
  const [holdings, setHoldings] = useState<string[]>();
  const [fundings, setFundings] = useState<string[]>();

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

        if (!traderName && !portfolioName) return;

        setPortfolio(getPortfolioByName(traderName, portfolioName));

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
        const netValueResult = sqlDB.exec(
          'select trade_date, net_value from portfolio_net_value_ledger order by trade_date desc limit 1'
        )[0];
        // @ts-ignore
        setLatestTradeDate(netValueResult.values[0][0]);
        // @ts-ignore
        setNetValue(netValueResult.values[0][1]);
        // @ts-ignore
        const firstTradeDate = sqlDB.exec(
          'select trade_date from portfolio_funding_ledger order by trade_date asc limit 1'
        )[0].values[0][0]; // @ts-ignore
        setFirstFundingDate(firstTradeDate);
        // @ts-ignore
        const portfolioPerformance: string[] = sqlDB.exec(
          'select retracement_range, max_retracement_range, cagr, sharpe_ratio, total_trade_count, days_of_win, days_of_loss, run_days from portfolio_performance_ledger order by trade_date desc limit 1'
        )[0].values[0]; // @ts-ignore
        setPerformance(portfolioPerformance);
        // @ts-ignore
        const portfolioTransactions: string[] = sqlDB.exec(
          'select trade_date, trade_code, trade_name, trade_type, trade_amount, trade_price, trade_money from portfolio_transaction_ledger order by trade_date desc'
        )[0].values; // @ts-ignore
        setTransactions(portfolioTransactions);
        // @ts-ignore
        const portfolioHoldings: string[] = sqlDB.exec(
          'select trade_date, trade_code, trade_name, hold_amount, close_price, market_value from portfolio_holding_ledger order by trade_date desc limit 1000'
        )[0].values; // @ts-ignore
        setHoldings(portfolioHoldings);
        // @ts-ignore
        const portfolioFundings: string[] = sqlDB.exec(
          'select trade_date, fund_type, fund_amount from portfolio_funding_ledger order by trade_date desc'
        )[0].values; // @ts-ignore
        setFundings(portfolioFundings);
        const optionsData = {
          grid: {
            top: 100,
            right: 10,
            bottom: 24,
            left: 40,
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
            min: 'dataMin',
            max: 'dataMax',
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
      <div className="flex flex-col items-center justify-center mb-10">
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

        {!loading && (
          <div className="flex flex-row flex-wrap items-center justify-center w-3/4 sm:mb-0 mb-5">
            <div className="relative p-8 m-2 border-t-4 border-yellow-500 rounded-sm shadow-xl">
              <h5 className="text-4xl font-bold">{netValue}</h5>
              <p className="mt-4 text-lg font-medium text-gray-500">最新净值</p>
            </div>
            <div className="relative block p-8 m-2 border-t-4 border-yellow-500 rounded-sm shadow-xl">
              <h5 className="text-4xl font-bold">
                {/* 
                // @ts-ignore */}
                {(performance[2] * 100).toFixed(1)}%
              </h5>
              <p className="mt-4 text-lg font-medium text-gray-500">
                年复合收益率
              </p>
            </div>
            <div className="relative block p-8 m-2 border-t-4 border-yellow-500 rounded-sm shadow-xl">
              <h5 className="text-4xl font-bold">{performance?.[3]}</h5>
              <p className="mt-4 text-lg font-medium text-gray-500">夏普比率</p>
            </div>
            <div className="relative block p-8 m-2 border-t-4 border-yellow-500 rounded-sm shadow-xl">
              <h5 className="text-4xl font-bold">
                {/* 
                // @ts-ignore */}
                {(performance[0] * 100).toFixed(1)}%
              </h5>
              <p className="mt-4 text-lg font-medium text-gray-500">当前回撤</p>
            </div>
            <div className="relative block p-8 m-2 border-t-4 border-yellow-500 rounded-sm shadow-xl">
              <h5 className="text-4xl font-bold">
                {/* 
                // @ts-ignore */}
                {(performance[1] * 100).toFixed(1)}%
              </h5>
              <p className="mt-4 text-lg font-medium text-gray-500">
                历史最大回撤
              </p>
            </div>
          </div>
        )}

        {!loading && (
          <div className="hidden sm:flex flex-row flex-wrap items-center justify-center mb-10 w-3/4">
            <div className="relative block p-8 m-2 border-t-4 border-yellow-500 rounded-sm shadow-xl">
              <h5 className="text-xl font-bold">{performance?.[4]}</h5>
              <p className="mt-4 text-lg font-medium text-gray-500">
                总交易次数
              </p>
            </div>
            <div className="relative block p-8 m-2 border-t-4 border-yellow-500 rounded-sm shadow-xl">
              <h5 className="text-xl font-bold">{performance?.[5]}</h5>
              <p className="mt-4 text-lg font-medium text-gray-500">盈利天数</p>
            </div>
            <div className="relative block p-8 m-2 border-t-4 border-yellow-500 rounded-sm shadow-xl">
              <h5 className="text-xl font-bold">{performance?.[6]}</h5>
              <p className="mt-4 text-lg font-medium text-gray-500">亏损天数</p>
            </div>
            <div className="relative block p-8 m-2 border-t-4 border-yellow-500 rounded-sm shadow-xl">
              <h5 className="text-xl font-bold">{performance?.[7]}</h5>
              <p className="mt-4 text-lg font-medium text-gray-500">运行天数</p>
            </div>
            <div className="relative block p-8 m-2 border-t-4 border-yellow-500 rounded-sm shadow-xl">
              <h5 className="text-xl font-bold">{firstFundingDate}</h5>
              <p className="mt-4 text-lg font-medium text-gray-500">建仓日期</p>
            </div>
            <div className="relative block p-8 m-2 border-t-4 border-yellow-500 rounded-sm shadow-xl">
              <h5 className="text-xl font-bold">{latestTradeDate}</h5>
              <p className="mt-4 text-lg font-medium text-gray-500">更新日期</p>
            </div>
          </div>
        )}

        <div className="sm:w-9/12 w-11/12">
          {!loading && (
            <ReactECharts option={options} style={{ height: 800 }} />
          )}
        </div>

        <div className="sm:w-9/12 w-11/12 mt-20 mb-20">
          {!loading && (
            <nav className="flex text-base font-bold border-b border-gray-100">
              <button
                onClick={() => {
                  setCurrentTab('transaction');
                }}
                className={
                  currentTab === 'transaction'
                    ? 'p-4 -mb-px border-b border-current text-yellow-500'
                    : 'p-4 -mb-px border-b border-transparent hover:text-yellow-500'
                }
              >
                历史交易
              </button>

              <button
                onClick={() => {
                  setCurrentTab('holding');
                }}
                className={
                  currentTab === 'holding'
                    ? 'p-4 -mb-px border-b border-current text-yellow-500'
                    : 'p-4 -mb-px border-b border-transparent hover:text-yellow-500'
                }
              >
                历史持仓
              </button>

              <button
                onClick={() => {
                  setCurrentTab('funding');
                }}
                className={
                  currentTab === 'funding'
                    ? 'p-4 -mb-px border-b border-current text-yellow-500'
                    : 'p-4 -mb-px border-b border-transparent hover:text-yellow-500'
                }
              >
                资金流水
              </button>
            </nav>
          )}
          {currentTab === 'transaction' && (
            <div className="overflow-x-auto mt-5">
              <table className="min-w-full text-sm border border-gray-100 divide-y-2 divide-gray-200">
                <thead>
                  <tr className="divide-x divide-gray-100">
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      日期
                    </th>
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      代码
                    </th>
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      名称
                    </th>
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      类型
                    </th>
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      数量
                    </th>
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      价格
                    </th>
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      金额
                    </th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-gray-200">
                  {transactions?.map((transaction, i) => (
                    <tr className="divide-x divide-gray-100" key={i}>
                      <td className="px-4 py-2 font-medium text-gray-900 whitespace-nowrap">
                        {transaction[0]}
                      </td>
                      <td className="px-4 py-2 text-gray-700 whitespace-nowrap">
                        {transaction[1]}
                      </td>
                      <td className="px-4 py-2 text-gray-700 whitespace-nowrap">
                        {transaction[2]}
                      </td>
                      <td className="px-4 py-2 text-gray-700 whitespace-nowrap">
                        {transaction[3]}
                      </td>
                      <td className="px-4 py-2 text-gray-700 whitespace-nowrap">
                        {transaction[4]}
                      </td>
                      <td className="px-4 py-2 text-gray-700 whitespace-nowrap">
                        {transaction[5]}
                      </td>
                      <td className="px-4 py-2 text-gray-700 whitespace-nowrap">
                        {transaction[6]}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          {currentTab === 'holding' && (
            <div className="overflow-x-auto mt-5">
              <table className="min-w-full text-sm border border-gray-100 divide-y-2 divide-gray-200">
                <thead>
                  <tr className="divide-x divide-gray-100">
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      日期
                    </th>
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      代码
                    </th>
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      名称
                    </th>
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      持仓数量
                    </th>
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      收盘价
                    </th>
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      市值
                    </th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-gray-200">
                  {holdings?.map((holding, i) => (
                    <tr className="divide-x divide-gray-100" key={i}>
                      <td className="px-4 py-2 font-medium text-gray-900 whitespace-nowrap">
                        {holding[0]}
                      </td>
                      <td className="px-4 py-2 text-gray-700 whitespace-nowrap">
                        {holding[1]}
                      </td>
                      <td className="px-4 py-2 text-gray-700 whitespace-nowrap">
                        {holding[2]}
                      </td>
                      <td className="px-4 py-2 text-gray-700 whitespace-nowrap">
                        {holding[3]}
                      </td>
                      <td className="px-4 py-2 text-gray-700 whitespace-nowrap">
                        {holding[4]}
                      </td>
                      <td className="px-4 py-2 text-gray-700 whitespace-nowrap">
                        {holding[5]}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          {currentTab === 'funding' && (
            <div className="overflow-x-auto mt-5">
              <table className="min-w-full text-sm border border-gray-100 divide-y-2 divide-gray-200">
                <thead>
                  <tr className="divide-x divide-gray-100">
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      日期
                    </th>
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      类型
                    </th>
                    <th className="px-4 py-2 font-medium text-left text-gray-900 whitespace-nowrap">
                      金额
                    </th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-gray-200">
                  {fundings?.map((funding, i) => (
                    <tr className="divide-x divide-gray-100" key={i}>
                      <td className="px-4 py-2 font-medium text-gray-900 whitespace-nowrap">
                        {funding[0]}
                      </td>
                      <td className="px-4 py-2 text-gray-700 whitespace-nowrap">
                        {funding[1]}
                      </td>
                      <td className="px-4 py-2 text-gray-700 whitespace-nowrap">
                        {funding[2]}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export { Portfolio };
