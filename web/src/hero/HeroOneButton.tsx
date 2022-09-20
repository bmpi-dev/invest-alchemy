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
              交易信号订阅
            </h2>

            <p className="text-gray-500 sm:mt-4">
              目前仅支持双均线策略信号的订阅，未来会支持多种交易策略信号
            </p>
          </div>

          {errorMsg !== '' && (
            <div
              className="p-4 text-red-700 border rounded border-red-900/10 bg-red-50 mt-2"
              role="alert"
            >
              <strong className="text-sm font-medium"> {errorMsg} </strong>
            </div>
          )}

          <div className="max-w-xl mx-auto mt-8">
            <form action="#" className="sm:gap-4 sm:flex">
              <div className="sm:flex-1">
                <label htmlFor="email" className="sr-only">
                  Email
                </label>

                <input
                  type="email"
                  placeholder="邮箱"
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full p-3 text-gray-700 bg-white border-gray-200 transition rounded-md shadow-sm focus:ring focus:outline-none focus:ring-yellow-400 focus:border-white"
                />
              </div>

              <button
                type="button"
                onClick={subscribeSNS}
                className="flex items-center justify-center w-full px-5 py-3 mt-4 text-white transition rounded-md bg-rose-600 sm:mt-0 sm:w-auto group focus:outline-none focus:ring focus:ring-yellow-400"
              >
                <span className="text-sm font-medium"> 订阅 </span>

                <svg
                  className="w-5 h-5 ml-3"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M17 8l4 4m0 0l-4 4m4-4H3"
                  />
                </svg>
              </button>
            </form>
          </div>
        </div>
      </aside>
    </header>
  );
};

export { HeroOneButton };
