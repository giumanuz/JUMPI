import { Image } from './image';

export type Article = {
  title: string;
  author: string;
  content: string;
  images: Image[];
  page_offsets: number[];
  page_range: number[];
};