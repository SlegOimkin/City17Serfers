// Basic Three.js infinite runner in a Half-Life inspired setting
let scene, camera, renderer;
let player, lane = 0;
const lanes = [-2, 0, 2];
const obstacles = [];
let speed = 0.1;
let score = 0;
let running = true;

function init() {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  // lighting
  const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1);
  scene.add(light);

  // ground
  const groundGeo = new THREE.PlaneGeometry(20, 1000);
  const groundMat = new THREE.MeshPhongMaterial({ color: 0x333333 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.position.z = -500;
  scene.add(ground);

  // player
  const playerGeo = new THREE.BoxGeometry(1, 2, 1);
  const playerMat = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
  player = new THREE.Mesh(playerGeo, playerMat);
  player.position.y = 1;
  scene.add(player);

  // citadel horizon
  const citadelGeo = new THREE.CylinderGeometry(1, 4, 50, 4);
  const citadelMat = new THREE.MeshPhongMaterial({ color: 0x5555ff });
  const citadel = new THREE.Mesh(citadelGeo, citadelMat);
  citadel.position.z = -200;
  citadel.position.y = 25;
  scene.add(citadel);

  camera.position.z = 5;

  window.addEventListener('resize', onWindowResize);
  document.addEventListener('keydown', onKeyDown);

  animate();
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

function spawnObstacle() {
  const obstacleGeo = new THREE.BoxGeometry(1, 2, 1);
  const obstacleMat = new THREE.MeshPhongMaterial({ color: 0xff0000 });
  const obstacle = new THREE.Mesh(obstacleGeo, obstacleMat);
  const laneIndex = Math.floor(Math.random() * lanes.length);
  obstacle.position.x = lanes[laneIndex];
  obstacle.position.y = 1;
  obstacle.position.z = -100;
  scene.add(obstacle);
  obstacles.push(obstacle);
}

function onKeyDown(event) {
  if (!running && event.key.toLowerCase() === 'r') {
    restart();
    return;
  }
  if (!running) return;
  if (event.key === 'ArrowLeft') {
    lane = Math.max(0, lane - 1);
  } else if (event.key === 'ArrowRight') {
    lane = Math.min(lanes.length - 1, lane + 1);
  }
  player.position.x = lanes[lane];
}

function animate() {
  if (running && Math.random() < 0.02) spawnObstacle();

  obstacles.forEach((ob, idx) => {
    ob.position.z += speed * 10;
    if (ob.position.z > camera.position.z) {
      scene.remove(ob);
      obstacles.splice(idx, 1);
      score += 10;
      document.getElementById('score').textContent = score;
    }
    if (ob.position.distanceTo(player.position) < 1.2) {
      running = false;
      document.getElementById('gameover').style.display = 'block';
    }
  });

  camera.position.z += speed * 10;
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}

function restart() {
  obstacles.forEach(ob => scene.remove(ob));
  obstacles.length = 0;
  camera.position.z = 5;
  player.position.x = 0;
  lane = 1;
  score = 0;
  speed = 0.1;
  running = true;
  document.getElementById('score').textContent = '0';
  document.getElementById('gameover').style.display = 'none';
}

init();
