type ScanResult = {
  page: number;
  text: string;
  comparisonImage: string;
};

type ArticleUploadResult = {
  articleId: string;
  scanResults: ScanResult[];
};
