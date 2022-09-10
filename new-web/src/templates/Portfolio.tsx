import { Meta } from '../layout/Meta';
import { AppConfig } from '../utils/AppConfig';
import { Footer } from './Footer';
import { Header } from './Header';

const Portfolio = () => (
  <div className="antialiased text-gray-600">
    <Meta
      title={AppConfig.title}
      description={AppConfig.description}
      canonical={AppConfig.canonical}
    />
    <Header />
    <Footer />
  </div>
);

export { Portfolio };
