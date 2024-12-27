import {Component, ViewEncapsulation} from '@angular/core';
import { GalleriaModule } from 'primeng/galleria';

@Component({
  selector: 'app-workflow-tutorial',
  templateUrl: './workflow-tutorial.component.html',
  styleUrls: ['./workflow-tutorial.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class WorkflowTutorialComponent {
  visible: boolean = false;
  dashboardStatus: boolean = false;
  images: any[] | undefined;
  images2: any[] | undefined;

  responsiveOptions: any[] | undefined;

  constructor() {
    this.images = [
      {
        itemImageSrc: 'assets/images/tutorial/dashboard-0.png',
        thumbnailImageSrc: 'assets/images/tutorial/dashboard-0.png',
        alt: '',
        title: ''
      },
      {
        itemImageSrc: 'assets/images/tutorial/dashboard-1.png',
        thumbnailImageSrc: 'assets/images/tutorial/dashboard-1.png',
        alt: '',
        title: ''
      },
      {
        itemImageSrc: 'assets/images/tutorial/dashboard-2.png',
        thumbnailImageSrc: 'assets/images/tutorial/dashboard-2.png',
        alt: '',
        title: ''
      },
      {
        itemImageSrc: 'assets/images/tutorial/dashboard-3.png',
        thumbnailImageSrc: 'assets/images/tutorial/dashboard-3.png',
        alt: '',
        title: ''
      },
    ];
    this.images2 = [
      {
        itemImageSrc: 'assets/images/tutorial/workflow-dash-0.png',
        thumbnailImageSrc: 'assets/images/tutorial/workflow-dash-0.png',
        alt: '',
        title: ''
      },
      {
        itemImageSrc: 'assets/images/tutorial/workflow-dash-1.png',
        thumbnailImageSrc: 'assets/images/tutorial/workflow-dash-1.png',
        alt: '',
        title: ''
      },
      {
        itemImageSrc: 'assets/images/tutorial/workflow-dash-2.png',
        thumbnailImageSrc: 'assets/images/tutorial/workflow-dash-2.png',
        alt: '',
        title: ''
      },
      {
        itemImageSrc: 'assets/images/tutorial/workflow-dash-3.png',
        thumbnailImageSrc: 'assets/images/tutorial/workflow-dash-3.png',
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

  changeDashboardStatus() {
    this.dashboardStatus = !this.dashboardStatus;
  }
}
