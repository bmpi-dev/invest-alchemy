import { ReactNode } from 'react';

type Link = {
  href: string;
  text: string;
};

type ISectionProps = {
  title?: string;
  description?: string;
  moreLink?: Link;
  yPadding?: string;
  children?: ReactNode;
};

const Section = (props: ISectionProps) => (
  <div
    className={`max-w-screen-lg mx-auto px-3 ${
      props.yPadding ? props.yPadding : 'py-6'
    }`}
  >
    {(props.title || props.description || props.moreLink) && (
      <div className="mb-6 text-center">
        {props.title && (
          <h2 className="text-4xl text-primary-500 font-bold">{props.title}</h2>
        )}
        {props.description && (
          <div className="mt-4 text-xl md:px-20">{props.description}</div>
        )}
        {props.moreLink && (
          <a className="text-red-400" href={props.moreLink.href}>
            {props.moreLink.text}
          </a>
        )}
      </div>
    )}

    {props.children}
  </div>
);

export { Section };
