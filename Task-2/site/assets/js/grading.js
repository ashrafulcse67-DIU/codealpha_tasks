/* Bangladesh grading rules, shared by the GPA, CGPA and SSC/HSC pages. */
(function () {
  'use strict';
  /* SSC/HSC (general education boards): marks out of 100 -> letter grade, grade point */
  var BOARD = [
    { min: 80, l: 'A+', gp: 5 }, { min: 70, l: 'A', gp: 4 }, { min: 60, l: 'A-', gp: 3.5 },
    { min: 50, l: 'B', gp: 3 }, { min: 40, l: 'C', gp: 2 }, { min: 33, l: 'D', gp: 1 }, { min: 0, l: 'F', gp: 0 }
  ];
  /* University (UGC 4.00 scale) */
  var UNI = [
    { min: 80, l: 'A+', gp: 4 }, { min: 75, l: 'A', gp: 3.75 }, { min: 70, l: 'A-', gp: 3.5 },
    { min: 65, l: 'B+', gp: 3.25 }, { min: 60, l: 'B', gp: 3 }, { min: 55, l: 'B-', gp: 2.75 },
    { min: 50, l: 'C+', gp: 2.5 }, { min: 45, l: 'C', gp: 2.25 }, { min: 40, l: 'D', gp: 2 }, { min: 0, l: 'F', gp: 0 }
  ];
  function fromMarks(marks) {
    for (var i = 0; i < BOARD.length; i++) if (marks >= BOARD[i].min) return BOARD[i];
  }
  /* Final GPA letter from the overall board GPA */
  function boardLetter(g) {
    return g >= 5 ? 'A+' : g >= 4 ? 'A' : g >= 3.5 ? 'A-' : g >= 3 ? 'B' : g >= 2 ? 'C' : g >= 1 ? 'D' : 'F';
  }
  function uniLetter(g) {
    return g >= 4 ? 'A+' : g >= 3.75 ? 'A' : g >= 3.5 ? 'A-' : g >= 3.25 ? 'B+' : g >= 3 ? 'B' : g >= 2.75 ? 'B-' : g >= 2.5 ? 'C+' : g >= 2.25 ? 'C' : g >= 2 ? 'D' : 'F';
  }
  /*
   * Board GPA with 4th subject.
   * subjects: [{gp:Number, fourth:Boolean}]
   * - Failing (GP 0) in any compulsory subject means GPA 0.00.
   * - 4th subject adds only (GP - 2) when GP > 2; it never lowers the GPA.
   * - Total points / number of compulsory subjects, capped at 5.00.
   */
  function boardGPA(subjects) {
    var main = subjects.filter(function (s) { return !s.fourth; });
    var fourth = subjects.filter(function (s) { return s.fourth; })[0];
    if (!main.length) return null;
    var base = main.reduce(function (a, s) { return a + s.gp; }, 0);
    var failed = main.some(function (s) { return s.gp === 0; });
    var bonus = fourth && fourth.gp > 2 ? fourth.gp - 2 : 0;
    var gpa = failed ? 0 : Math.min(5, (base + bonus) / main.length);
    return { gpa: gpa, failed: failed, bonus: bonus, base: base, count: main.length, hasFourth: !!fourth, fourthGP: fourth ? fourth.gp : null };
  }
  window.BD = { BOARD: BOARD, UNI: UNI, fromMarks: fromMarks, boardLetter: boardLetter, uniLetter: uniLetter, boardGPA: boardGPA };
})();
