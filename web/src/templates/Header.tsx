import Link from 'next/link';
import { useRouter } from 'next/router';

import { Meta } from '../layout/Meta';
import { Section } from '../layout/Section';
import { NavbarTwoColumns } from '../navigation/NavbarTwoColumns';
import { AppConfig } from '../utils/AppConfig';
import { Logo } from './Logo';

const Header = () => {
  const router = useRouter();
  return (
    <div className="antialiased text-gray-600">
      <Meta
        title={AppConfig.title}
        description={AppConfig.description}
        canonical={router.asPath}
      />
      <Section yPadding="py-6">
        <NavbarTwoColumns logo={<Logo xl />}>
          <li className="text-sm sm:text-xl">
            <Link href="mailto:me@i365.tech" className="mr-2">
              <a>付费订阅</a>
            </Link>
          </li>
          <li className="text-sm sm:text-xl">
            <Link href="https://www.bmpi.dev/money/" className="mr-2">
              <a>组合报告</a>
            </Link>
          </li>
        </NavbarTwoColumns>
      </Section>
    </div>
  );
};

export { Header };
