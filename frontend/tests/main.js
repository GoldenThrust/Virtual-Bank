const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

function flowCard(type, amount, profit, x, y) {
    ctx.roundRect(x, y, 100, 200, 20);
    console.log(ctx);
    ctx.fillStyle = 'red';
    ctx.fillText(type, x, y);
}


flowCard("investment", 500000, 20, 20, 20)