import Controller from '@ember/controller';
import { computed } from '@ember/object';

import { isEmpty } from '@ember/utils';
export default Controller.extend({

  poem: "",

  disabled: true,
  categories_list: ['Category 1', 'Category 2', 'Category 3'],
  selected_category: "",

  errorMessage: "",

  generatingState: false,
  generatingLabel: 'Generating..',


  progress_value: 0,
  _interval: null,
  startTime: 0,
  timer: Ember.computed('progress_value', function() {
    const that = this;
    if (this._interval === null) {
      this.set('startTime', Date.now());
      this._interval = setInterval(function() {
        that.set('progress_value', that.get('progress_value') + 1);
      }, 100);
    }

    return this.get('progress_value');
  }),

  actions:{
    getPoem(){
      let self = this;
      this.get('timer');
      self.set('progress_value', 0);
      self.set('generatingState', true);
      self.set('errorMessage', "");
      if( isEmpty(self.get('selected_category'))) {
        this.set('errorMessage', "Please select a category!")
        self.set('generatingState', false);
      }

      var cat;
      if(this.get('selected_category')==="Category 1")
        cat = "1";
      else if(this.get('selected_category')==="Category 2")
        cat = "2";
      else if(this.get('selected_category')==="Category 3")
        cat = "3";
      console.log(cat);
      Ember.$.ajax({
        url: `http://localhost:5000/`,
        type: "GET",
        data: {
          category: cat
        },
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function(resp){


        console.log(resp['poem']);
        var poem = resp['poem'];
        // poem = poem.split('\n').join('<br>');
        // poem = poem.split('\n\\\n\n').join('<br><br>');
        self.set('poem', poem);
        self.set('errorMessage', "");

      }).catch(function(error){
        console.log("negative");

      });
    }

  }

});
