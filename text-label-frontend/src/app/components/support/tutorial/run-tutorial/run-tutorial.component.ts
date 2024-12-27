import {Component, ViewEncapsulation} from '@angular/core';

@Component({
  selector: 'app-run-tutorial',
  templateUrl: './run-tutorial.component.html',
  styleUrls: ['./run-tutorial.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class RunTutorialComponent {

  visible: boolean = false;
  images: any[] | undefined;

  responsiveOptions: any[] | undefined;

  constructor() {
    this.images = [
      {
        itemImageSrc: 'assets/images/tutorial/step1.jpg',
        thumbnailImageSrc: 'assets/images/tutorial/step1.jpg',
        alt: '',
        title: ''
      },
      {
        itemImageSrc: 'assets/images/tutorial/step2.jpg',
        thumbnailImageSrc: 'assets/images/tutorial/step2.jpg',
        alt: '',
        title: ''
      },
      {
        itemImageSrc: 'assets/images/tutorial/step3.jpg',
        thumbnailImageSrc: 'assets/images/tutorial/step3.jpg',
        alt: '',
        title: ''
      },
      {
        itemImageSrc: 'assets/images/tutorial/step4.jpg',
        thumbnailImageSrc: 'assets/images/tutorial/step4.jpg',
        alt: '',
        title: ''
      },
    ];
    this.responsiveOptions = [
      {
        breakpoint: '1024px',
        numVisible: 5
      },
      {
        breakpoint: '768px',
        numVisible: 3
      },
      {
        breakpoint: '560px',
        numVisible: 1
      }
    ];
  }

  showDialog() {
    this.visible = true;
  }

}
