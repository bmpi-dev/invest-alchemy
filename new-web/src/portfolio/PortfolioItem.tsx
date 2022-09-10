import className from 'classnames';
import Link from 'next/link';
import { useRouter } from 'next/router';

type IPortfolioProps = {
  title: string;
  description: string;
  link: string;
  netValue: string;
  updateDate: string;
  createDate: string;
  image: string;
  imageAlt: string;
  reverse?: boolean;
};

const PortfolioItem = (props: IPortfolioProps) => {
  const verticalFeatureClass = className(
    'mt-20',
    'flex',
    'flex-wrap',
    'items-center',
    {
      'flex-row-reverse': props.reverse,
    }
  );

  const router = useRouter();

  return (
    <div className={verticalFeatureClass}>
      <div className="w-full sm:w-1/2 text-center sm:text-left sm:px-6">
        <button className="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded">
          <Link href={props.link}>{props.title}</Link>
        </button>

        <div className="mt-6 text-sm leading-9">{props.description}</div>
        <div className="mt-auto text-base leading-9">
          当前净值：{props.netValue}
        </div>
        <div className="mt-auto text-base leading-9">
          更新时间：{props.updateDate}
        </div>
        <div className="mt-auto text-base leading-9">
          创建时间：{props.createDate}
        </div>
      </div>

      <div className="w-full sm:w-1/2 p-6">
        <img src={`${router.basePath}${props.image}`} alt={props.imageAlt} />
      </div>
    </div>
  );
};

export { PortfolioItem };
