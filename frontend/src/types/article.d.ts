type ArticlePageScan = {
  page: number;
  imageData: string;
  uploadedOn: Date;
};

type ArticleFigure = {
  page: number;
  caption: string;
  imageData: string;
};

type Article = {
  id: string;
  magazineId: string;
  title: string;
  author: string;
  content: string;
  pageRange: number[];
  pageOffsets: number[];
  pageScans: ArticlePageScan[];
  figures: ArticleFigure[];
  createdOn: Date;
  editedOn: Date;
};

type ArticleResultPage = {
  scanResults: { comparisonImage: string; page: number }[];
  text: string;
  figures: ArticleFigure[];
  pageScans: ArticlePageScan[];
};
