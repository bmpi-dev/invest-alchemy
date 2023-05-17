import { ReactNode, useState } from 'react';

type IHeroOneButtonProps = {
  title: ReactNode;
  description: string;
  button: ReactNode;
};

const HeroOneButton = (props: IHeroOneButtonProps) => {
  const [email, setEmail] = useState<string>('');
  const [errorMsg, setErrorMsg] = useState<string>('');

  let timeoutId: any;

  const setErrMsg = (err: string, timeSecond = 2000) => {
    if (timeoutId !== null) {
      clearTimeout(timeoutId);
    }
    setErrorMsg(err);
    timeoutId = setTimeout(() => {
      setErrorMsg('');
      timeoutId = null;
    }, timeSecond);
  };

  const subscribeSNS = () => {
    if (email != null && email !== '') {
      setErrMsg('正在请求...');
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      };
      fetch(
        'https://fey17sm0g7.execute-api.us-east-1.amazonaws.com/dev/subscribe',
        requestOptions
      )
        .then((response) => response.json())
        .then((data) => {
          const r = JSON.parse(data);
          const body = JSON.parse(r.body);
          if (body.code !== 0) {
            setErrMsg(body.message);
          } else {
            setErrMsg(
              '即将订阅成功，请在邮件里确认订阅（邮件标题：AWS Notifications），如果没收到，请在垃圾箱中检查！',
              3000
            );
          }
        });
    } else {
      setErrMsg('请填写邮箱！');
    }
  };

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
              付费请发邮件至 me@i365.tech 来信咨询
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
