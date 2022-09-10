import { useRouter } from 'next/router';

import { Section } from '../layout/Section';
import { PortfolioItem } from '../portfolio/PortfolioItem';

const Portfolios = () => {
  const router = useRouter();

  return (
    <Section title="投资组合">
      <PortfolioItem
        title="1号投资组合"
        description="机器人自动跟随投资策略交易，跟随11/22日双均线投资策略，投资标的为场内ETF指数基金。"
        link={`${router.basePath}/portfolio?t=robot_dma_v01&p=dma_11_22`}
        netValue={'1.0'}
        updateDate={''}
        createDate={''}
        image="/assets/images/feature.svg"
        imageAlt="1号投资组合"
      />
      <PortfolioItem
        title="2号投资组合"
        description="机器人自动跟随投资策略交易，跟随11/22日双均线投资策略，投资标的为创业板(399006.SZ)指数基金。"
        link={`${router.basePath}/portfolio?t=robot_dma_v02&p=dma_11_22`}
        netValue={'1.0'}
        updateDate={''}
        createDate={''}
        image="/assets/images/feature2.svg"
        imageAlt="2号投资组合"
        reverse
      />
      <PortfolioItem
        title="被动收入投资组合"
        description="被动收入组合旨在以最小交易维护成本做进取型长期投资，期望通过投资获得被动收入，保障家庭财务状况健康。投资标的：各类ETF，包括宽基指数、行业指数等。也会拿出不超过组合10%的占比来投资（投机）风险更高的加密货币。投资市场：中国、香港及美国。"
        link={`${router.basePath}/portfolio?t=bmpi&p=被动收入`}
        netValue={'1.0'}
        updateDate={''}
        createDate={''}
        image="/assets/images/feature3.svg"
        imageAlt="被动收入投资组合"
      />
    </Section>
  );
};

export { Portfolios };
