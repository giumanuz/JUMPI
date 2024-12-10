type ScanResult = {
  page: number;
  comparisonImage: string;
};

type ArticleUploadResult = {
  articleId: string;
  text: string;
  scanResults: ScanResult[];
};
