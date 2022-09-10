import { Meta } from '../layout/Meta';
import { Section } from '../layout/Section';
import { AppConfig } from '../utils/AppConfig';
import { Footer } from './Footer';
import { Hero } from './Hero';
import { Portfolios } from './Portfolios';

const link = {
  href: 'https://www.bmpi.dev/money/road_to_trading/',
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
    <Footer />
  </div>
);

export { Base };
