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
          <li>
            <Link
              href="https://github.com/bmpi-dev/invest-alchemy"
              className="mr-2"
            >
              <a>GitHub</a>
            </Link>
          </li>
          <li>
            <Link href="https://t.me/improve365">
              <a>Telegram</a>
            </Link>
          </li>
        </NavbarTwoColumns>
      </Section>
    </div>
  );
};

export { Header };
