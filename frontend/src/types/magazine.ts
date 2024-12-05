import { Article } from './article';

type Magazine = {
  name: string;
  year: number;
  publisher: string;
  genre: string;
  articles: Article[];
  abstract: string;
};