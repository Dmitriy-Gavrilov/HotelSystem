#ifndef FINDROOMBYEQUIPMENTFORM_H
#define FINDROOMBYEQUIPMENTFORM_H

#include <QWidget>

#include "baseform.h"

namespace Ui {
class FindRoomByEquipmentForm;
}

class FindRoomByEquipmentForm : public QWidget, public BaseForm
{
    Q_OBJECT

public:
    explicit FindRoomByEquipmentForm(QWidget *parent = nullptr);
    ~FindRoomByEquipmentForm();

    void clear() override;

signals:
    void sendData(const QString &data);

private slots:
    void on_FindRoomByEquipmentBtn_clicked();

private:
    Ui::FindRoomByEquipmentForm *ui;
};

#endif // FINDROOMBYEQUIPMENTFORM_H
