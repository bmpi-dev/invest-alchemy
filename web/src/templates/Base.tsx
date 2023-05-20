import { Meta } from '../layout/Meta';
import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';
import { Footer } from './Footer';
import { Hero } from './Hero';
import { Portfolios } from './Portfolios';

const link = {
  href: 'https://www.bmpi.dev/money/invest-alchemy/',
  text: '👉进一步了解',
};

const Base = () => (
  <div className="antialiased text-gray-600">
    <Meta
      title={AppConfig.title}
      description={AppConfig.description}
      canonical={AppConfig.canonical}
    />
    <Hero />
    <Section
      title="设计理念"
      description="要想在变幻莫测充满不确定性的市场中稳定的盈利，我们需要有自己性格可以驾驭的交易系统才行。一个好的交易系统应该具备风险评估、资金管理及交易策略，同时需要适应交易者的交易心理。"
      moreLink={link}
    ></Section>
    <Portfolios />
    <Section title="重要问题">
      <div className="space-y-4">
        <details className="group">
          <summary className="flex items-center justify-between p-4 rounded-lg cursor-pointer bg-gray-50">
            <h5 className="font-medium text-gray-900">投资炼金术是什么？</h5>

            <svg
              className="flex-shrink-0 ml-1.5 w-5 h-5 transition duration-300 group-open:-rotate-180"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </summary>

          <p className="px-4 mt-4 leading-relaxed text-gray-700">
            为了满足上班族或业余投资者简单长期的投资需求，投资炼金术这个辅助用户投资交易的系统，它可以从投资组合整体的角度评价交易策略的风险与收益，而不像大多量化投资软件，解决了交易策略在模拟回测与投资组合实践中差距过大的问题。
          </p>
        </details>

        <details className="group">
          <summary className="flex items-center justify-between p-4 rounded-lg cursor-pointer bg-gray-50">
            <h5 className="font-medium text-gray-900">
              跟市面上的量化软件有何区别？
            </h5>

            <svg
              className="flex-shrink-0 ml-1.5 w-5 h-5 transition duration-300 group-open:-rotate-180"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </summary>

          <p className="px-4 mt-4 leading-relaxed text-gray-700">
            投资炼金术更偏向于投资组合的整体风险与收益评价，很多量化软件更专注与策略开发回测，并不适合普通投资者。这个系统更专注于：简单策略与长期投资。它可以评估投资组合整体的风险与回报率，而量化软件更关注某个策略的表现而非投资组合整体。
          </p>
        </details>

        <details className="group">
          <summary className="flex items-center justify-between p-4 rounded-lg cursor-pointer bg-gray-50">
            <h5 className="font-medium text-gray-900">
              交易策略过拟合的问题怎么解决？
            </h5>

            <svg
              className="flex-shrink-0 ml-1.5 w-5 h-5 transition duration-300 group-open:-rotate-180"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </summary>

          <p className="px-4 mt-4 leading-relaxed text-gray-700">
            回测过拟合可能是交易策略无法应对市场多变的主要原因，所以交易策略的调优不应通过过拟合来追求收益最大化，简单的交易策略与分散的投资标的可以克服市场的未知波动。以双均线为例，可以按
            11/22
            参数去回测，也可以不断调整这个值去找最优的过拟合参数，但用任何的参数来说都可以，因为它是一个趋势跟随的策略，优缺点都很明确：适合趋势行情，在震荡行情就是成本，小亏博大赢，注定它是一个胜率不高但盈亏比很高的策略。所以说如果如果有调优的话，就是让参数或策略更粗糙一些，策略越简单、组合交易标的越多，这个策略的稳定性更强，虽然收益率可能要低一些，但只要比同期全球主流指数的排名中等偏上就可以了（因为我们无法预知某个指数未来收益率的高低），这也是投资炼金术关注的核心：
            <span className="font-bold text-yellow-500">
              关注投资组合整体而非某个策略
            </span>
            。
          </p>
        </details>

        <details className="group">
          <summary className="flex items-center justify-between p-4 rounded-lg cursor-pointer bg-gray-50">
            <h5 className="font-medium text-gray-900">
              为什么交易策略在模拟和真实之间存在很大的偏差？
            </h5>

            <svg
              className="flex-shrink-0 ml-1.5 w-5 h-5 transition duration-300 group-open:-rotate-180"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </summary>

          <p className="px-4 mt-4 leading-relaxed text-gray-700">
            模拟回测与实际交易之间存在一条鸿沟，这是由多种原因造成的：
            <span className="font-bold">
              停牌或交易额很低造成的流动性问题、交易滑点、策略过拟合
            </span>
            。对于投资炼金术来说，由于其交易标的大多是指数 ETF
            基金，所以不存在停牌、流动性或滑点的问题，至于过拟合的问题，在上述也有介绍。总体来说，选择交易指数
            ETF
            而非股票，让我们规避了很多模拟交易与真实交易差距过大的问题，当然市场瞬息万变，就像战场一样，模拟战玩的再好，实战可能被秒杀。这也是我们需要不断提升个人交易能力的原因，这也是交易的魅力所在，这也是投资炼金术被创造的原因：
            <span className="font-bold">
              通过给投资组合设定监控指标，发现投资组合的整体风险，进而不断提升交易者的个人交易能力，最终帮助大家打造一个健康的财务状况
            </span>
            。
          </p>
        </details>

        <details className="group">
          <summary className="flex items-center justify-between p-4 rounded-lg cursor-pointer bg-gray-50">
            <h5 className="font-medium text-gray-900">
              为什么指数 ETF 基金相比股票与公募基金更适合普通投资者？
            </h5>

            <svg
              className="flex-shrink-0 ml-1.5 w-5 h-5 transition duration-300 group-open:-rotate-180"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </summary>

          <p className="px-4 mt-4 leading-relaxed text-gray-700">
            指数基金是一揽子股票的集合，相比个股风险本来就低：不存在莫名其妙的停牌、不存在流动性的问题、不存在暴雷的可能性（不考虑经济的宏观风险）。普通投资者的劣势在于：没有专业性、没有时间、资金少，但优势也有，那就是我们可以做到长期投资，随着收入的逐渐增加，我们投资水平的提升，财务状况会通过投资得到持续的改善。从这个角度讲，选择指数基金要比个股风险更低，能获取行业与国家成长的红利。投资个股你需要担惊受怕，潜在的把自己的精力给消耗掉了，导致浪费了很多宝贵的时间。另外一个重要的原因是，大多数人投资的本金并不多，把自己宝贵的时间浪费在个股选择上而非工作或副业的打造上，这种丢了西瓜捡芝麻的行为并不可取。
          </p>
          <p className="px-4 mt-4 leading-relaxed text-gray-700">
            那公募基金为什么不适合？选公募基金犹如选白马，好的公募基金的确有更出彩的投资能力，选择公募基金理论上也的确更适合普通投资者，但这里存在一个屁股决定脑袋的问题：公募基金盈利的核心是收取管理费，这意味着公募基金盈利的关键在于把盘子做的更大，吸引更多投资者投入资金。如何吸引呢？那就是在牛市末期疯狂发行基金，而这恰恰是亏损的根源，在市场顶峰入局就算交易大师来了也要被套牢。而且公募基金背后的基金经理可能会离职或换人（好的公募基金经理大概率会被私募基金高薪挖走，或者自己搞私募，因为收入会暴增），导致你辛苦选择的白马可能变成驴。
          </p>
        </details>

        <details className="group">
          <summary className="flex items-center justify-between p-4 rounded-lg cursor-pointer bg-gray-50">
            <h5 className="font-medium text-gray-900">
              机器人模拟交易投资组合的注意事项
            </h5>

            <svg
              className="flex-shrink-0 ml-1.5 w-5 h-5 transition duration-300 group-open:-rotate-180"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </summary>

          <p className="px-4 mt-4 leading-relaxed text-gray-700">
            <span className="font-bold">滑点</span>
            ：由于交易的标的物是场内指数 ETF 基金，因此交易滑点问题的影响很小。
          </p>
          <p className="px-4 mt-4 leading-relaxed text-gray-700">
            <span className="font-bold">分红</span>
            ：机器人交易员会忽略持仓分红的情况（ETF
            指数基金一般不分红），因为计算会比较复杂。但是，真实的用户交易者可以手动将股息记录为一笔价格为零的买入交易。
          </p>
          <p className="px-4 mt-4 leading-relaxed text-gray-700">
            <span className="font-bold">费用</span>
            ：由于 A 股市场的 ETF/LOF
            交易费用非常低，所以机器人交易员为了简化计算而忽略交易费用。
          </p>
          <p className="px-4 mt-4 leading-relaxed text-gray-700">
            <span className="font-bold">流动性</span>
            ：因为模拟交易无法得知当天交易的流动性，比如 A
            股涨跌幅限制导致无法成交，与实际交易存在一定偏差，这也是真实交易的魅力所在，存在一定的不确定性，是盈亏同源的所在。
          </p>
          <p className="px-4 mt-4 leading-relaxed text-gray-700">
            <span className="font-bold">复权</span>
            ：机器人交易员会在跟随交易信号产生交易记录台账时，处理复权的问题。真实用户的投资组合可自行处理复权问题，一般券商的系统会自动买入或卖出一笔价格为
            0 的交易记录来处理因价格复权导致的持仓数量变化问题。
          </p>
        </details>
      </div>
    </Section>
    <Footer />
  </div>
);

export { Base };
