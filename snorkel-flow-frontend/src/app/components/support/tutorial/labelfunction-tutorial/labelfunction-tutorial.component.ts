import {Component, ViewEncapsulation} from '@angular/core';

@Component({
  selector: 'app-labelfunction-tutorial',
  templateUrl: './labelfunction-tutorial.component.html',
  styleUrls: ['./labelfunction-tutorial.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class LabelfunctionTutorialComponent {
  visible: boolean = false;

  images: any[] | undefined;

  responsiveOptions: any[] | undefined;

  constructor() {
    this.images = [
      {
        itemImageSrc: 'assets/images/tutorial/labelfunction-editor-0.png',
        thumbnailImageSrc: 'assets/images/tutorial/labelfunction-editor-0.png',
        alt: '',
        title: ''
      },
      {
        itemImageSrc: 'assets/images/tutorial/labelfunction-editor-1.png',
        thumbnailImageSrc: 'assets/images/tutorial/labelfunction-editor-1.png',
        alt: '',
        title: ''
      },
      {
        itemImageSrc: 'assets/images/tutorial/labelfunction-editor-2.png',
        thumbnailImageSrc: 'assets/images/tutorial/labelfunction-editor-2.png',
        alt: '',
        title: ''
      },
      {
        itemImageSrc: 'assets/images/tutorial/labelfunction-editor-3.png',
        thumbnailImageSrc: 'assets/images/tutorial/labelfunction-editor-3.png',
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
