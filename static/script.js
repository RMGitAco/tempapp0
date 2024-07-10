document.getElementById('uploadForm').addEventListener('submit', function(event) {
  event.preventDefault();
  
  const frontFile = document.getElementById('front_image').files[0];
  const backFile = document.getElementById('back_image').files[0];

  if (frontFile && backFile) {
    const reader1 = new FileReader();
    const reader2 = new FileReader();

    reader1.onload = function(event1) {
      const frontImage = new Image();
      frontImage.src = event1.target.result;
      frontImage.onload = function() {
        reader2.onload = function(event2) {
          const backImage = new Image();
          backImage.src = event2.target.result;
          backImage.onload = function() {
            combineImages(frontImage, backImage);
          };
        };
        reader2.readAsDataURL(backFile);
      };
    };
    reader1.readAsDataURL(frontFile);
  }
});

function combineImages(frontImage, backImage) {
  const borderSize = 10;
  const canvas = document.createElement('canvas');
  const combinedWidth = frontImage.width + backImage.width + borderSize * 3;
  const combinedHeight = Math.max(frontImage.height, backImage.height) + borderSize * 2;

  canvas.width = combinedWidth;
  canvas.height = combinedHeight;
  const ctx = canvas.getContext('2d');
  
  ctx.fillStyle = 'white';
  ctx.fillRect(0, 0, combinedWidth, combinedHeight);

  ctx.drawImage(frontImage, borderSize, borderSize);
  ctx.drawImage(backImage, frontImage.width + 2 * borderSize, borderSize);

  const combinedImageURL = canvas.toDataURL('image/jpeg');
  document.getElementById('combinedImage').src = combinedImageURL;
  document.getElementById('downloadButton').href = combinedImageURL;

  document.getElementById('result').style.display = 'block';
  
  // Replace the Combine Now button with the Download Combined Image button
  document.getElementById('combineButton').style.display = 'none';
  document.getElementById('downloadButton').style.display = 'inline-block';
}
