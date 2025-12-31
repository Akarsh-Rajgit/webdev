let score = 0;
let hits = 0;
const maxHits = 50;
const winScore = 100;
let gameRunning = true;

const player = document.getElementById("player");
const enemiesContainer = document.getElementById("enemies-container");
const scoreDisplay = document.getElementById("score");
const hitsDisplay = document.getElementById("hits");
const gameOverDisplay = document.getElementById("game-over");
const winDisplay = document.getElementById("win-message");


document.addEventListener("keydown", (e) => {
    const playerY = player.offsetTop;
    if (e.key === "ArrowUp" && playerY > 0) {
        player.style.top = (playerY - 20) + "px";
    } else if (e.key === "ArrowDown" && playerY < window.innerHeight - 50) {
        player.style.top = (playerY + 20) + "px";
    }
});


function spawnEnemy() {
    if (!gameRunning) return;

    const enemy = document.createElement("div");
    enemy.classList.add(Math.random() > 0.5 ? "enemy" : "asteroid");
    enemy.style.left = window.innerWidth + "px";
    enemy.style.top = Math.random() * (window.innerHeight - 50) + "px";
    enemiesContainer.appendChild(enemy);

    let moveInterval = setInterval(() => {
        const enemyX = enemy.offsetLeft - 5;
        enemy.style.left = enemyX + "px";

        if (
            enemyX <= player.offsetLeft + 50 &&
            enemyX >= player.offsetLeft - 40 &&
            enemy.offsetTop >= player.offsetTop - 40 &&
            enemy.offsetTop <= player.offsetTop + 50
        ) {
            if (enemy.classList.contains("enemy")) {
                score--;
                hits++;
            } else {
                hits++;
            }
            updateStats();
            clearInterval(moveInterval);
            enemy.remove();
        }

        if (enemyX < -50) {
            clearInterval(moveInterval);
            enemy.remove();
        }

        if (hits >= maxHits) {
            gameOver();
        } else if (score >= winScore) {
            winGame();
        }
    }, 30);
}

function updateStats() {
    scoreDisplay.textContent = `Score: ${score}`;
    hitsDisplay.textContent = `Hits: ${hits}/${maxHits}`;
}

function gameOver() {
    gameRunning = false;
    gameOverDisplay.style.display = "block";
}

function winGame() {
    gameRunning = false;
    winDisplay.style.display = "block";
}

setInterval(spawnEnemy, 1000);
setInterval(() => {
    if (gameRunning) {
        const enemies = document.querySelectorAll(".enemy, .asteroid");
        enemies.forEach(enemy => {
            if (enemy.offsetLeft < -50) {
                enemy.remove();
            }
        });
    }
}, 1000);
document.addEventListener("keydown", (e) => {
    if (e.key === " " && gameRunning) {
        const bullet = document.createElement("div");
        bullet.style.position = "absolute";
        bullet.style.width = "10px";
        bullet.style.height = "5px";
        bullet.style.background = "yellow";
        bullet.style.left = (player.offsetLeft + 50) + "px";
        bullet.style.top = (player.offsetTop + 25) + "px";
        document.body.appendChild(bullet);

        let bulletInterval = setInterval(() => {
            const bulletX = bullet.offsetLeft + 10;
            bullet.style.left = bulletX + "px";

            document.querySelectorAll(".enemy").forEach(enemy => {
                if (
                    bulletX >= enemy.offsetLeft &&
                    bulletX <= enemy.offsetLeft + 40 &&
                    bullet.offsetTop >= enemy.offsetTop &&
                    bullet.offsetTop <= enemy.offsetTop + 40
                ) {
                    score++;
                    updateStats();
                    enemy.remove();
                    bullet.remove();
                    clearInterval(bulletInterval);
                }
            });

            if (bulletX > window.innerWidth) {
                bullet.remove();
                clearInterval(bulletInterval);
            }
        }, 30);
    }
});