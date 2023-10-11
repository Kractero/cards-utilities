// ==UserScript==
// @name        Auto Login Upload Flag
// @namespace   Violentmonkey Scripts
// @match       https://www.nationstates.net/*test=1*
// @grant       none
// @version     1.0
// @author      Kractero
// ==/UserScript==
(function() {
    'use strict';
    let enpass = document.querySelectorAll('input[type="password"]')[1];
    if (enpass) {
      enpass.value = "PASSWORDGLASSWORD!!!!!!!!!!!!!!!!!!!";
      let check = document.querySelectorAll('input[type="checkbox"]')[1];
      if (check) {
        check.click();
      }
      let button = document.querySelectorAll("button")[1];
      if (button) {
        button.focus();
      }
    }
})();
