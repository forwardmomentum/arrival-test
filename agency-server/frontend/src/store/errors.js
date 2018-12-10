export default (error) => {
  console.error(`[ERROR] ${error}`);
  if (error.response && error.response.data) {
    const message = error.response.data.message || '';
    checkSize(message);
    throw error.response.data.message;
  }
};

const checkSize = (message) => {
  if (message.toLowerCase().includes('maximum upload size exceeded')) {
    throw 'Превышен размер загружаемого файла';
  }
};