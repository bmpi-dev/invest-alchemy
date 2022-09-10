import { useRouter } from 'next/router';

import { Section } from '../layout/Section';
import { PortfolioItem } from '../portfolio/PortfolioItem';
import { PortfolioConfig } from '../utils/PortfolioConfig';

const Portfolios = () => {
  const router = useRouter();

  return (
    <Section title="投资组合">
      <PortfolioItem
        title={PortfolioConfig.p1.title}
        description={PortfolioConfig.p1.description}
        link={`${router.basePath}/portfolio?t=${PortfolioConfig.p1.traderName}&p=${PortfolioConfig.p1.portfolioName}`}
        netValue={''}
        updateDate={''}
        createDate={''}
        image="/assets/images/feature.svg"
        imageAlt={PortfolioConfig.p1.title}
      />
      <PortfolioItem
        title={PortfolioConfig.p2.title}
        description={PortfolioConfig.p2.description}
        link={`${router.basePath}/portfolio?t=${PortfolioConfig.p2.traderName}&p=${PortfolioConfig.p2.portfolioName}`}
        netValue={''}
        updateDate={''}
        createDate={''}
        image="/assets/images/feature2.svg"
        imageAlt={PortfolioConfig.p2.title}
        reverse
      />
      <PortfolioItem
        title={PortfolioConfig.p3.title}
        description={PortfolioConfig.p3.description}
        link={`${router.basePath}/portfolio?t=${PortfolioConfig.p3.traderName}&p=${PortfolioConfig.p3.portfolioName}`}
        netValue={''}
        updateDate={''}
        createDate={''}
        image="/assets/images/feature3.svg"
        imageAlt={PortfolioConfig.p3.title}
      />
    </Section>
  );
};

export { Portfolios };
