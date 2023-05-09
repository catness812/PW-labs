<template>
  <div id="app">
    <router-view />
    <div class="anime-container"></div>
  </div>
</template>

<script>
// check if quiz was/is played DONE
// resume quiz DONE
// quiz timer DONE
// show elapsed time DONE
// back to welcome page button DONE
// logout button on welcome page DONE
// background music DONE
// custom messages for certain scores DONE
// mouse trail DONE

import anime from "animejs";

export default {
  name: "App",

  mounted() {
    var container = document.querySelector(".anime-container");

    var sparks = [];
    var sparksIndex = 0;
    var sparkCount = 100;
    var sparkParticleCount = 6;

    function lerp(p1, p2, t) {
      return p1 + (p2 - p1) * t;
    }

    const ease = {
      linear: (t) => t,
      inQuad: (t) => t * t,
      outQuad: (t) => t * (2 - t),
      inOutQuad: (t) => (t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t),
      inCubic: (t) => t * t * t,
      outCubic: (t) => --t * t * t + 1,
      inOutCubic: (t) =>
        t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1,
      inQuart: (t) => t * t * t * t,
      outQuart: (t) => 1 - --t * t * t * t,
      inOutQuart: (t) =>
        t < 0.5 ? 8 * t * t * t * t : 1 - 8 * --t * t * t * t,
      inQuint: (t) => t * t * t * t * t,
      outQuint: (t) => 1 + --t * t * t * t * t,
      inOutQuint: (t) =>
        t < 0.5 ? 16 * t * t * t * t * t : 1 + 16 * --t * t * t * t * t,
    };

    function circularRandom(r) {
      r = r * Math.sqrt(Math.abs(Math.random() - Math.random()));
      var theta = Math.random() * 2 * Math.PI;
      var x = r * Math.cos(theta);
      var y = r * Math.sin(theta);
      return { x: x, y: y, r: r };
    }

    for (var i = 0; i <= sparkCount; i += 1) {
      var spark = { els: [] };

      for (var j = 0; j < sparkParticleCount; j++) {
        var dot = document.createElement("div");
        dot.classList.add("dot");
        container.appendChild(dot);
        spark.els.push(dot);

        var particleSize = anime.random(3, 10);
        var sparkRadius = 15;
        var { x, y, r } = circularRandom(sparkRadius);

        dot.style.width =
          lerp(particleSize, 1, ease.outQuad(r / sparkRadius)) + "px";
        dot.style.height =
          lerp(particleSize, 1, ease.outQuad(r / sparkRadius)) + "px";
        dot.style.opacity = "0";
        dot.style.transform = "translateX(" + x + "px) translateY(" + y + "px)";
      }

      spark.anime = new anime({
        targets: spark.els,
        loop: false,
        easing: "linear",
        autoplay: false,
        delay: anime.stagger(8),
        opacity: [
          { value: 0, duration: 0 },
          { value: 1, duration: 40 },
          {
            value: 0,
            duration: function () {
              return anime.random(500, 800);
            },
          },
        ],
        width: { value: 2, duration: 500 },
        height: { value: 2, duration: 500 },
        translateX: {
          value: function () {
            return anime.random(-30, 30);
          },
          duration: 800,
        },
        translateY: {
          value: function () {
            return anime.random(-30, 30);
          },
          duration: 800,
        },
      });
      sparks.push(spark);
    }

    window.addEventListener(
      "mousemove",
      function (e) {
        anime.set(sparks[sparksIndex].els, {
          left: e.pageX,
          top: e.pageY,
        });
        sparks[sparksIndex].anime.restart();
        sparksIndex++;
        if (sparksIndex == sparks.length) sparksIndex = 0;
      },
      false
    );
  },
};
</script>

<style>
@font-face {
  font-family: "HarryPotter";
  src: url("@/assets/harry_potter/harryp-webfont.woff2") format("woff2"),
    url("@/assets/harry_potter/harryp-webfont.woff2") format("woff");
}

* {
  font-family: "HarryPotter", Arial, sans-serif;
}

body {
  overflow: hidden;
}

.anime-container {
  position: relative;
}

.anime-container .dot {
  position: absolute;
  border-radius: 40%;
  background-color: #fde5aa;
}
</style>