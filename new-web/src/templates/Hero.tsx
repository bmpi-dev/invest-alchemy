import Link from 'next/link';

import { Background } from '../background/Background';
import { Button } from '../button/Button';
import { HeroOneButton } from '../hero/HeroOneButton';
import { Section } from '../layout/Section';
import { NavbarTwoColumns } from '../navigation/NavbarTwoColumns';
import { Logo } from './Logo';

const Hero = () => (
  <Background color="bg-gray-100">
    <Section yPadding="py-6">
      <NavbarTwoColumns logo={<Logo xl />}>
        <li className="text-sm sm:text-xl">
          <Link
            href="https://github.com/bmpi-dev/invest-alchemy"
            className="mr-2"
          >
            <a>GitHub</a>
          </Link>
        </li>
        <li className="text-sm sm:text-xl">
          <Link href="https://t.me/improve365">
            <a>Telegram</a>
          </Link>
        </li>
      </NavbarTwoColumns>
    </Section>

    <Section yPadding="pt-20 pb-32">
      <HeroOneButton
        title={
          <>
            {'构建你的\n'}
            <span className="text-primary-500">交易系统</span>
          </>
        }
        description="交易策略 / 资金策略 / 风险评估 / 交易评测 / 投资组合"
        button={
          <Link href="https://money.i365.tech/">
            <a>
              <Button xl>订阅交易策略</Button>
            </a>
          </Link>
        }
      />
    </Section>
  </Background>
);

export { Hero };
