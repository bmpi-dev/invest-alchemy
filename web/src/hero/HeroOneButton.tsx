import { ReactNode, useState } from 'react';

type IHeroOneButtonProps = {
  title: ReactNode;
  description: string;
  button: ReactNode;
};

const HeroOneButton = (props: IHeroOneButtonProps) => {
  return (
    <header className="text-center">
      <h1 className="text-5xl text-gray-900 font-bold whitespace-pre-line leading-hero">
        {props.title}
      </h1>
      <div className="text-2xl mt-4 mb-16">{props.description}</div>

      <aside className="bg-gray-50">
        <div className="p-8 md:p-12 lg:px-16 lg:py-24">
          <div className="max-w-lg mx-auto text-center">
            <h2 className="text-2xl font-bold text-gray-500 md:text-3xl">
              交易信号邮件提醒付费订阅
            </h2>

            <p className="text-red-500 sm:mt-4">
              付费请发邮件至 <me@i365.tech> 来信咨询
            </p>

            <p className="text-gray-500 sm:mt-2">
              目前仅支持双均线策略信号的订阅，未来会支持多种交易策略信号
            </p>
          </div>
        </div>
      </aside>
    </header>
  );
};

export { HeroOneButton };
