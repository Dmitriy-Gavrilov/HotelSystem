#include "departform.h"
#include "ui_departform.h"

DepartForm::DepartForm(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::DepartForm)
{
    ui->setupUi(this);
}

DepartForm::~DepartForm()
{
    delete ui;
}

void DepartForm::clear()
{
    this->ui->passport->clear();
    this->ui->roomId->clear();
    this->ui->dateMoveIn->setDate(QDate::fromString("01.01.2024", "dd.MM.yyyy"));
    this->ui->dateDepart->setDate(QDate::fromString("01.01.2024", "dd.MM.yyyy"));
}

void DepartForm::on_pushButton_clicked()
{
    QString data = "depart;" + this->ui->roomId->text() + ";" + this->ui->passport->text() + ";" +
                   this->ui->dateMoveIn->text() + ";" + this->ui->dateDepart->text();
    emit sendData(data);
}

