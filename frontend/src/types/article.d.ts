type ArticlePageScan = {
  page: number;
  imageData: string;
  uploadedOn: Date;
}

type ArticleFigure = {
  page: number;
  caption: string;
  imageData: string;
}

type Article = {
  id: string;
  magazineId: string;
  title: string;
  author: string;
  content: string;
  pageOffsets: number[];
  pageRange: number[];
  pageScans: ArticlePageScan[];
  figures: ArticleFigure[];
  createdOn: Date;
  editedOn: Date;
};
