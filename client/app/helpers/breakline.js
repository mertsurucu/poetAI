import { helper } from '@ember/component/helper';

export function breakline([str]) {
  let div = document.createElement('div');
    str.split('\n').forEach((str) => {
      div.appendChild(document.createTextNode(str));
      div.appendChild(document.createElement('br' && 'p'));
  });

  return Ember.String.htmlSafe(div.innerHTML);
}


export default helper(breakline);
